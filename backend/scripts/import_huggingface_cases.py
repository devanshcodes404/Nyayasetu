"""
Command-line batch importer for Hugging Face Indian case-law dataset.
Run via:
python scripts/import_huggingface_cases.py --limit 100 --batch-size 50
python scripts/import_huggingface_cases.py --limit 100 --dry-run
"""
import sys
import os
import argparse
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.services.legal_dataset.importer import DatasetImporter
from app.core.config import settings


def main():
    parser = argparse.ArgumentParser(description="NyayaSetu AI Indian Case-Law Dataset Importer")
    parser.add_argument("--dataset-id", default=settings.HF_DATASET_ID, help="Hugging Face Dataset ID")
    parser.add_argument("--config", default=settings.HF_DATASET_CONFIG, help="Dataset configuration")
    parser.add_argument("--split", default=settings.HF_DATASET_SPLIT, help="Dataset split (train, etc.)")
    parser.add_argument("--limit", type=int, default=settings.HF_IMPORT_LIMIT, help="Max records to examine")
    parser.add_argument("--batch-size", type=int, default=settings.HF_IMPORT_BATCH_SIZE, help="Database batch insert size")
    parser.add_argument("--dry-run", action="store_true", help="Simulate import without committing to database")
    parser.add_argument("--no-resume", action="store_true", help="Disable import resumption")
    parser.add_argument("--report-dir", default="../data/import-reports", help="Directory for JSON import reports")

    args = parser.parse_args()

    print("=" * 60)
    print("NYAYASETU AI — DATASET INGESTION PIPELINE")
    print(f"Dataset ID:  {args.dataset_id}")
    print(f"Split:       {args.split}")
    print(f"Limit:       {args.limit}")
    print(f"Batch Size:  {args.batch_size}")
    print(f"Dry Run:     {args.dry_run}")
    print(f"Resumable:   {not args.no_resume}")
    print("=" * 60)

    db = SessionLocal()
    try:
        importer = DatasetImporter(
            db=db,
            dataset_id=args.dataset_id,
            config=args.config,
            split=args.split,
            streaming=settings.HF_DATASET_STREAMING,
            batch_size=args.batch_size,
            limit=args.limit,
            dry_run=args.dry_run,
            resume=not args.no_resume,
        )

        result = importer.run()

        print("\n--- INGESTION RESULTS ---")
        print(f"Job Status:  {result['status']}")
        print(f"Examined:    {result['examined']}")
        print(f"Imported:    {result['imported']}")
        print(f"Updated:     {result['updated']}")
        print(f"Skipped:     {result['skipped']}")
        print(f"Rejected:    {result['rejected']}")
        if result.get("error_summary"):
            print(f"Error Note:  {result['error_summary']}")

        # Save import report to data/import-reports/
        os.makedirs(args.report_dir, exist_ok=True)
        report_file = os.path.join(args.report_dir, f"report_job_{result.get('job_id', 'unknown')}.json")
        with open(report_file, "w", encoding="utf-8") as rf:
            json.dump(result, rf, indent=2)
        print(f"Report saved to: {report_file}")

    finally:
        db.close()


if __name__ == "__main__":
    main()

