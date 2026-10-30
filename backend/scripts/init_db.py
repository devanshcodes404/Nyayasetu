"""
Initialize database tables.
Can be executed directly via Python CLI:
python scripts/init_db.py
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.base import Base
from app.db.session import engine
import app.models  # Register all models


def init_db():
    print(f"Creating all database tables on engine: {engine.url}")
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized successfully.")


if __name__ == "__main__":
    init_db()

