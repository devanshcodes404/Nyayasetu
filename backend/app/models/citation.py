"""
LegalCitation database model for tracked and extracted legal authorities.
"""
from typing import Optional
from sqlalchemy import String, Text, Integer, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class LegalCitation(Base, TimestampMixin):
    __tablename__ = "citations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Source where citation appeared
    document_id: Mapped[Optional[int]] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), nullable=True, index=True)
    judgment_id: Mapped[Optional[int]] = mapped_column(ForeignKey("judgments.id", ondelete="CASCADE"), nullable=True, index=True)
    
    # Referenced judgment if resolved in database
    referenced_judgment_id: Mapped[Optional[int]] = mapped_column(ForeignKey("judgments.id", ondelete="SET NULL"), nullable=True, index=True)
    
    raw_citation: Mapped[str] = mapped_column(String(500), nullable=False)
    normalized_citation: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, index=True)
    context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    page_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    verification_status: Mapped[str] = mapped_column(String(50), default="Unverified", nullable=False)  # Verified, Unverified, Ambiguous, NotFound

    # Relationships
    document: Mapped[Optional["LegalDocument"]] = relationship("LegalDocument", back_populates="citations")
    judgment: Mapped[Optional["Judgment"]] = relationship(
        "Judgment",
        foreign_keys=[judgment_id],
        back_populates="citations",
    )
    referenced_judgment: Mapped[Optional["Judgment"]] = relationship(
        "Judgment",
        foreign_keys=[referenced_judgment_id],
    )

    __table_args__ = (
        Index("idx_citation_lookup", "normalized_citation"),
    )

