"""
Database session management.
Supports PostgreSQL (with pgvector) in production/local setup, and fallbacks to SQLite for dev/test.
"""
from typing import Generator
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.core.logging import logger

# Construct database engine safely
if settings.DATABASE_URL:
    db_url = settings.DATABASE_URL
    # Handle postgres:// vs postgresql:// dialect naming in some hosting environments
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+"):
        db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
    
    if "sqlite" in db_url:
        engine = create_engine(db_url, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(
            db_url,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            pool_pre_ping=True,
        )
else:
    # Development fallback: SQLite file in current backend or memory
    dev_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "nyayasetu_dev.db"))
    engine = create_engine(
        f"sqlite:///{dev_db_path}",
        connect_args={"check_same_thread": False},
    )
    logger.info(f"DATABASE_URL not set; using local development database at sqlite:///{dev_db_path}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency that yields a database session and safely closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

