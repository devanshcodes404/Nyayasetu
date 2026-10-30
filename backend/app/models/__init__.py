"""
Model registry exporting all SQLAlchemy database entities.
"""
from app.db.base import Base
from app.models.user import User
from app.models.case import LegalCase
from app.models.document import LegalDocument
from app.models.judgment import Judgment
from app.models.chunk import DocumentChunk
from app.models.citation import LegalCitation
from app.models.dataset_import import DatasetImportJob

__all__ = [
    "Base",
    "User",
    "LegalCase",
    "LegalDocument",
    "Judgment",
    "DocumentChunk",
    "LegalCitation",
    "DatasetImportJob",
]

