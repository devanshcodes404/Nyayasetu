"""
Court Case request and response schemas.
"""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class CaseCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    case_number: str = Field(..., min_length=2, max_length=100)
    court: str = Field(..., min_length=2, max_length=255)
    jurisdiction: str = Field(default="State", max_length=100)
    case_type: str = Field(default="Civil", max_length=100)
    client_name: str = Field(..., min_length=2, max_length=255)
    opposing_party: str = Field(..., min_length=2, max_length=255)
    status: str = Field(default="Active", max_length=50)
    filing_date: Optional[date] = None
    next_hearing_date: Optional[date] = None
    description: Optional[str] = None


class CaseUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    case_number: Optional[str] = Field(None, min_length=2, max_length=100)
    court: Optional[str] = Field(None, min_length=2, max_length=255)
    jurisdiction: Optional[str] = None
    case_type: Optional[str] = None
    client_name: Optional[str] = None
    opposing_party: Optional[str] = None
    status: Optional[str] = None
    filing_date: Optional[date] = None
    next_hearing_date: Optional[date] = None
    description: Optional[str] = None


class CaseResponse(BaseModel):
    id: int
    owner_id: int
    title: str
    case_number: str
    court: str
    jurisdiction: str
    case_type: str
    client_name: str
    opposing_party: str
    status: str
    filing_date: Optional[date] = None
    next_hearing_date: Optional[date] = None
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    documents_count: Optional[int] = 0

    class Config:
        from_attributes = True

