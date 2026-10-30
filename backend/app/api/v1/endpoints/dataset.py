"""
Dataset status endpoint.
Reports total judgments imported, text coverage, and latest import job metrics.
Does NOT run full corpus imports over HTTP.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.judgment import Judgment
from app.models.dataset_import import DatasetImportJob
from app.schemas.dataset import DatasetStatusResponse
from app.core.config import settings

router = APIRouter()


@router.get("/status", response_model=DatasetStatusResponse)
def get_dataset_status(db: Session = Depends(get_db)):
    total = db.query(func.count(Judgment.id)).scalar() or 0
    full_text = db.query(func.count(Judgment.id)).filter(Judgment.text_availability_status == "FullText").scalar() or 0
    headnotes = db.query(func.count(Judgment.id)).filter(Judgment.text_availability_status == "HeadnoteOnly").scalar() or 0
    metadata_only = db.query(func.count(Judgment.id)).filter(Judgment.text_availability_status == "MetadataOnly").scalar() or 0
    courts = db.query(func.count(func.distinct(Judgment.court_name))).scalar() or 0

    latest_job = (
        db.query(DatasetImportJob)
        .order_by(DatasetImportJob.id.desc())
        .first()
    )

    latest_job_data = None
    if latest_job:
        latest_job_data = {
            "id": latest_job.id,
            "status": latest_job.status,
            "is_dry_run": latest_job.is_dry_run,
            "records_imported": latest_job.records_imported,
            "records_examined": latest_job.records_examined,
            "started_at": latest_job.started_at.isoformat() if latest_job.started_at else None,
            "completed_at": latest_job.completed_at.isoformat() if latest_job.completed_at else None,
        }

    return DatasetStatusResponse(
        dataset_id=settings.HF_DATASET_ID,
        total_judgments_imported=total,
        judgments_with_full_text=full_text,
        judgments_with_headnotes=headnotes,
        metadata_only_judgments=metadata_only,
        courts_represented=courts,
        latest_import_job=latest_job_data,
        storage_type="PostgreSQL (indexed text + metadata)",
        is_ready_for_search=total > 0,
    )

