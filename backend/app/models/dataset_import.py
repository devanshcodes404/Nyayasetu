"""
DatasetImportJob database model for tracking Hugging Face batch ingestion jobs.
"""
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy import String, Integer, DateTime, Text, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class DatasetImportJob(Base, TimestampMixin):
    __tablename__ = "dataset_import_jobs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dataset_id: Mapped[str] = mapped_column(String(255), nullable=False)
    configuration: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    split: Mapped[str] = mapped_column(String(50), default="train", nullable=False)
    
    status: Mapped[str] = mapped_column(String(50), default="Pending", nullable=False)  # Pending, Running, Completed, Failed, Cancelled
    is_dry_run: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    records_examined: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    records_imported: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    records_updated: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    records_skipped: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    records_rejected: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    last_processed_external_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    error_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    job_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

