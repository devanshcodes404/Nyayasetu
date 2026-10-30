"""
Judgment database model for real Indian case law corpus records.
Stores metadata, citations, benches, full text or headnotes, provenance, and source links.
"""
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import String, Text, Date, DateTime, Integer, JSON, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class Judgment(Base, TimestampMixin):
    __tablename__ = "judgments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Dataset Provenance & Identifiers
    source_dataset: Mapped[str] = mapped_column(String(100), default="Sumitedu/indian-case-laws", nullable=False, index=True)
    external_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    case_metadata_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    parser_record_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    dataset_source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    ingestion_split: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Core Case Info
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    petitioner: Mapped[Optional[str]] = mapped_column(String(300), nullable=True, index=True)
    respondent: Mapped[Optional[str]] = mapped_column(String(300), nullable=True, index=True)
    party_caption: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    docket_number: Mapped[Optional[str]] = mapped_column(String(150), nullable=True, index=True)
    cnr_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    
    # Citations
    neutral_citation: Mapped[Optional[str]] = mapped_column(String(150), nullable=True, index=True)
    law_report_citation: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)

    # Court & Bench Hierarchy
    court_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    court_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    jurisdiction: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    bench_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    presiding_judge: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    coram_members: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    coram_members_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Dates and Years
    decision_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)
    registration_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    decision_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    citation_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Outcomes & Text
    disposition_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    normalized_outcome: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)  # Allowed, Dismissed, Disposed, Remanded
    indexable_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    headnote_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Source Files & Upstream URLs
    source_pdf_s3_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    source_json_s3_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    source_relative_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    source_filename: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    source_path_court_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    source_path_bench: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    source_path_year: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    language_codes: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Quality & Text Availability Status
    text_availability_status: Mapped[str] = mapped_column(
        String(50),
        default="MetadataOnly",
        nullable=False,
        index=True
    )  # FullText, HeadnoteOnly, ShortIndexable, MetadataOnly, Inaccessible
    verification_status: Mapped[str] = mapped_column(String(50), default="UnverifiedSource", nullable=False)
    import_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Source Metadata JSON blobs
    normalized_record_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    parser_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    quality_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Relationships
    chunks: Mapped[List["DocumentChunk"]] = relationship("DocumentChunk", back_populates="judgment", cascade="all, delete-orphan")
    citations: Mapped[List["LegalCitation"]] = relationship(
        "LegalCitation",
        foreign_keys="LegalCitation.judgment_id",
        back_populates="judgment",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("idx_judgments_court_year", "court_name", "decision_year"),
        Index("idx_judgments_text_avail", "text_availability_status"),
        UniqueConstraint("source_dataset", "external_id", name="uq_dataset_external_id"),
    )

