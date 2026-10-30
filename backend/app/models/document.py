"""
LegalDocument database model for user-uploaded private case files.
"""
from typing import Optional, List
from sqlalchemy import String, Integer, BigInteger, Boolean, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class LegalDocument(Base, TimestampMixin):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    case_id: Mapped[Optional[int]] = mapped_column(ForeignKey("cases.id", ondelete="SET NULL"), nullable=True, index=True)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)  # Local relative path or Blob URL/key
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    sha256_checksum: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    
    processing_status: Mapped[str] = mapped_column(String(50), nullable=False, default="Uploaded")  # Uploaded, Parsing, Indexed, Failed
    page_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_public_judgment: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    text_availability_status: Mapped[str] = mapped_column(String(50), default="Pending", nullable=False)  # FullText, HeadnoteOnly, ScannedImage, Pending, Failed

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="documents")
    case: Mapped[Optional["LegalCase"]] = relationship("LegalCase", back_populates="documents")
    chunks: Mapped[List["DocumentChunk"]] = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    citations: Mapped[List["LegalCitation"]] = relationship("LegalCitation", back_populates="document", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_docs_owner_case", "owner_id", "case_id"),
    )

