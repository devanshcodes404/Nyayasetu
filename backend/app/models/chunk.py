"""
DocumentChunk database model for vector storage, text embeddings, and retrieval.
Enforces strict association with either a private LegalDocument or a public Judgment.
"""
from typing import Optional, Dict, Any
from sqlalchemy import Text, Integer, ForeignKey, JSON, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin

# Optional pgvector support; uses JSON/Text representation if pgvector extension is not compiled
try:
    from pgvector.sqlalchemy import Vector
    PGVECTOR_AVAILABLE = True
except ImportError:
    PGVECTOR_AVAILABLE = False


class DocumentChunk(Base, TimestampMixin):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    document_id: Mapped[Optional[int]] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), nullable=True, index=True)
    judgment_id: Mapped[Optional[int]] = mapped_column(ForeignKey("judgments.id", ondelete="CASCADE"), nullable=True, index=True)
    
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    page_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    chunk_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Embedding vector column (1536 dim default for OpenAI or similar compatible models)
    if PGVECTOR_AVAILABLE:
        embedding = mapped_column(Vector(1536).with_variant(JSON, "sqlite"), nullable=True)
    else:
        embedding = mapped_column(JSON, nullable=True)

    # Relationships
    document: Mapped[Optional["LegalDocument"]] = relationship("LegalDocument", back_populates="chunks")
    judgment: Mapped[Optional["Judgment"]] = relationship("Judgment", back_populates="chunks")

    __table_args__ = (
        CheckConstraint(
            "(document_id IS NOT NULL AND judgment_id IS NULL) OR (document_id IS NULL AND judgment_id IS NOT NULL)",
            name="chk_chunk_document_or_judgment",
        ),
        Index("idx_chunks_doc_chunk", "document_id", "chunk_index"),
        Index("idx_chunks_judg_chunk", "judgment_id", "chunk_index"),
    )

