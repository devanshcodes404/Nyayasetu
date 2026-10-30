"""
LegalCase database model for court case tracking and management.
"""
from datetime import date
from typing import Optional, List
from sqlalchemy import String, Text, Date, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class LegalCase(Base, TimestampMixin):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    case_number: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    court: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    jurisdiction: Mapped[str] = mapped_column(String(100), nullable=False, default="State")
    case_type: Mapped[str] = mapped_column(String(100), nullable=False, default="Civil")
    
    client_name: Mapped[str] = mapped_column(String(255), nullable=False)
    opposing_party: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Active", index=True)  # Active, Pending, Disposed, Appeal
    
    filing_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    next_hearing_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="cases")
    documents: Mapped[List["LegalDocument"]] = relationship("LegalDocument", back_populates="case", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_cases_owner_status", "owner_id", "status"),
    )

