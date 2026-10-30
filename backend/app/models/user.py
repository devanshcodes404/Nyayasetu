"""
User database model for authentication and multi-tenancy.
"""
from typing import List
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    cases: Mapped[List["LegalCase"]] = relationship("LegalCase", back_populates="owner", cascade="all, delete-orphan")
    documents: Mapped[List["LegalDocument"]] = relationship("LegalDocument", back_populates="owner", cascade="all, delete-orphan")

