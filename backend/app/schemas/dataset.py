"""
Schemas for dataset status and ingestion reporting.
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel


class DatasetStatusResponse(BaseModel):
    dataset_id: str
    total_judgments_imported: int
    judgments_with_full_text: int
    judgments_with_headnotes: int
    metadata_only_judgments: int
    courts_represented: int
    latest_import_job: Optional[Dict[str, Any]] = None
    storage_type: str
    is_ready_for_search: bool


class DatasetImportJobResponse(BaseModel):
    id: int
    dataset_id: str
    configuration: Optional[str] = None
    split: str
    status: str
    is_dry_run: bool
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    records_examined: int
    records_imported: int
    records_updated: int
    records_skipped: int
    records_rejected: int
    last_processed_external_id: Optional[str] = None
    error_summary: Optional[str] = None

    class Config:
        from_attributes = True

