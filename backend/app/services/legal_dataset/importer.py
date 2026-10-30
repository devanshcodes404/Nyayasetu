"""
Idempotent, resumable batch importer for Hugging Face Indian case-law dataset.
Tracks batch transactions, creates DatasetImportJob records, and prevents duplicates.
"""
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.judgment import Judgment
from app.models.dataset_import import DatasetImportJob
from app.services.legal_dataset.loader import DatasetLoader
from app.services.legal_dataset.mapping import map_raw_record_to_judgment
from app.services.legal_dataset.validation import validate_judgment_record
from app.core.logging import logger


class DatasetImporter:
    def __init__(
        self,
        db: Session,
        dataset_id: str = "Sumitedu/indian-case-laws",
        config: Optional[str] = None,
        split: str = "train",
        streaming: bool = True,
        batch_size: int = 100,
        limit: int = 100,
        dry_run: bool = False,
        resume: bool = True,
    ):
        self.db = db
        self.dataset_id = dataset_id
        self.config = config
        self.split = split
        self.streaming = streaming
        self.batch_size = batch_size
        self.limit = limit
        self.dry_run = dry_run
        self.resume = resume

    def run(self) -> Dict[str, Any]:
        """Runs the import job idempotently."""
        # Check for previous resume state
        last_id = None
        if self.resume:
            last_job = (
                self.db.query(DatasetImportJob)
                .filter(DatasetImportJob.dataset_id == self.dataset_id)
                .order_by(DatasetImportJob.id.desc())
                .first()
            )
            if last_job and last_job.last_processed_external_id:
                last_id = last_job.last_processed_external_id

        # Create tracking job
        job = DatasetImportJob(
            dataset_id=self.dataset_id,
            configuration=self.config,
            split=self.split,
            status="Running",
            is_dry_run=self.dry_run,
            started_at=datetime.now(timezone.utc),
            last_processed_external_id=last_id,
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)

        examined = 0
        imported = 0
        updated = 0
        skipped = 0
        rejected = 0
        error_summary = None

        loader = DatasetLoader(
            dataset_id=self.dataset_id,
            config=self.config,
            split=self.split,
            streaming=self.streaming,
        )

        batch = []
        try:
            for raw_record in loader.load_stream():
                if examined >= self.limit:
                    break
                examined += 1

                mapped = map_raw_record_to_judgment(raw_record, source_dataset=self.dataset_id)
                is_valid, reject_reason = validate_judgment_record(mapped)
                if not is_valid:
                    rejected += 1
                    continue

                ext_id = mapped.get("external_id")
                # Deduplication check in DB
                existing = None
                if ext_id:
                    existing = (
                        self.db.query(Judgment)
                        .filter(
                            Judgment.source_dataset == self.dataset_id,
                            Judgment.external_id == ext_id,
                        )
                        .first()
                    )

                if existing:
                    # Update fields if new content is richer
                    if not self.dry_run:
                        if not existing.indexable_text and mapped.get("indexable_text"):
                            existing.indexable_text = mapped["indexable_text"]
                            existing.text_availability_status = mapped["text_availability_status"]
                            updated += 1
                        else:
                            skipped += 1
                    else:
                        skipped += 1
                else:
                    if not self.dry_run:
                        judgment_obj = Judgment(
                            import_timestamp=datetime.now(timezone.utc),
                            **mapped,
                        )
                        batch.append(judgment_obj)
                        imported += 1

                        if len(batch) >= self.batch_size:
                            self.db.add_all(batch)
                            self.db.commit()
                            batch = []
                    else:
                        imported += 1

                if ext_id:
                    job.last_processed_external_id = ext_id

            # Flush remaining batch
            if batch and not self.dry_run:
                self.db.add_all(batch)
                self.db.commit()

            job.status = "Completed"
        except Exception as e:
            logger.error(f"Error during dataset import: {e}", exc_info=True)
            self.db.rollback()
            job.status = "Failed"
            error_summary = f"{type(e).__name__}: {str(e)}"
        finally:
            job.completed_at = datetime.now(timezone.utc)
            job.records_examined = examined
            job.records_imported = imported
            job.records_updated = updated
            job.records_skipped = skipped
            job.records_rejected = rejected
            job.error_summary = error_summary
            self.db.commit()

        return {
            "job_id": job.id,
            "status": job.status,
            "is_dry_run": self.dry_run,
            "examined": examined,
            "imported": imported,
            "updated": updated,
            "skipped": skipped,
            "rejected": rejected,
            "error_summary": error_summary,
        }

