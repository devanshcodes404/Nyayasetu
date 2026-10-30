"""
Citation schemas for extraction and verification endpoints.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CitationItemResponse(BaseModel):
    id: int
    raw_citation: str
    normalized_citation: Optional[str] = None
    context: Optional[str] = None
    page_number: Optional[int] = None
    verification_status: str
    referenced_judgment_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

