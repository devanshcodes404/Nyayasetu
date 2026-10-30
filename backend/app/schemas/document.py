"""
LegalDocument request and response schemas.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class DocumentResponse(BaseModel):
    id: int
    owner_id: int
    case_id: Optional[int] = None
    title: str
    original_filename: str
    mime_type: str
    file_size: int
    sha256_checksum: str
    processing_status: str
    page_count: Optional[int] = None
    is_public_judgment: bool
    source_url: Optional[str] = None
    text_availability_status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentUploadMetadata(BaseModel):
    case_id: Optional[int] = None
    title: Optional[str] = None

