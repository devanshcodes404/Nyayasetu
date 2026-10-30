"""
Judgment search, filter, and detailed view schemas.
"""
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class JudgmentSearchParams(BaseModel):
    q: Optional[str] = Field(None, description="Keyword search in title, party captions, or text")
    title: Optional[str] = None
    party: Optional[str] = Field(None, description="Search petitioner or respondent")
    citation: Optional[str] = Field(None, description="Search neutral citation or law report citation")
    case_number: Optional[str] = None
    cnr_number: Optional[str] = None
    court: Optional[str] = None
    jurisdiction: Optional[str] = None
    year: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    disposition: Optional[str] = None
    text_availability: Optional[str] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class JudgmentListItem(BaseModel):
    id: int
    title: str
    petitioner: Optional[str] = None
    respondent: Optional[str] = None
    party_caption: Optional[str] = None
    court_name: str
    docket_number: Optional[str] = None
    cnr_number: Optional[str] = None
    neutral_citation: Optional[str] = None
    law_report_citation: Optional[str] = None
    decision_date: Optional[date] = None
    decision_year: Optional[int] = None
    disposition_text: Optional[str] = None
    normalized_outcome: Optional[str] = None
    text_availability_status: str
    verification_status: str
    has_source_pdf: bool = False
    headnote_snippet: Optional[str] = None

    class Config:
        from_attributes = True


class JudgmentDetailResponse(BaseModel):
    id: int
    source_dataset: str
    external_id: Optional[str] = None
    case_metadata_id: Optional[str] = None
    parser_record_id: Optional[str] = None
    title: str
    petitioner: Optional[str] = None
    respondent: Optional[str] = None
    party_caption: Optional[str] = None
    docket_number: Optional[str] = None
    cnr_number: Optional[str] = None
    neutral_citation: Optional[str] = None
    law_report_citation: Optional[str] = None
    court_name: str
    court_code: Optional[str] = None
    jurisdiction: Optional[str] = None
    bench_name: Optional[str] = None
    presiding_judge: Optional[str] = None
    coram_members: Optional[str] = None
    coram_members_text: Optional[str] = None
    decision_date: Optional[date] = None
    registration_date: Optional[date] = None
    decision_year: Optional[int] = None
    citation_year: Optional[int] = None
    disposition_text: Optional[str] = None
    normalized_outcome: Optional[str] = None
    indexable_text: Optional[str] = None
    headnote_text: Optional[str] = None
    source_pdf_s3_url: Optional[str] = None
    source_json_s3_url: Optional[str] = None
    source_relative_path: Optional[str] = None
    language_codes: Optional[str] = None
    text_availability_status: str
    verification_status: str
    import_timestamp: Optional[datetime] = None
    quality_json: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

