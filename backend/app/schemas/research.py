"""
Schemas for legal research, RAG queries, summarization, citations, and outcome insights.
Clear contracts for PART 2 readiness.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ResearchQueryRequest(BaseModel):
    query: str = Field(..., min_length=5, description="Legal question or query")
    case_id: Optional[int] = Field(None, description="Optional private case context scope")
    scope: str = Field(default="all", description="public, private, or all")
    top_k: int = Field(default=5, ge=1, le=20)


class CitationSource(BaseModel):
    citation: str
    judgment_id: Optional[int] = None
    document_id: Optional[int] = None
    court: Optional[str] = None
    year: Optional[int] = None
    snippet: str
    relevance_score: Optional[float] = None


class ResearchQueryResponse(BaseModel):
    query: str
    status: str = "reserved_for_part_2"
    message: str
    provider: str
    answer: Optional[str] = None
    sources: List[CitationSource] = []
    scope_used: str
    processing_time_ms: Optional[float] = None


class JudgmentSummaryResponse(BaseModel):
    judgment_id: int
    status: str = "reserved_for_part_2"
    provider: str
    message: str
    case_title: Optional[str] = None
    summary_type: str = "comprehensive"
    headnote: Optional[str] = None
    key_legal_issues: List[str] = []
    held_disposition: Optional[str] = None
    notable_citations: List[str] = []


class SimilarCaseResult(BaseModel):
    judgment_id: int
    title: str
    court: str
    decision_date: Optional[str] = None
    similarity_score: float
    key_matching_factors: List[str] = []
    text_availability_status: str


class SimilarCasesResponse(BaseModel):
    case_id: int
    status: str = "reserved_for_part_2"
    message: str
    results: List[SimilarCaseResult] = []


class CitationExtractionResponse(BaseModel):
    document_id: int
    status: str = "reserved_for_part_2"
    message: str
    total_citations_found: int
    citations: List[Dict[str, Any]] = []


class OutcomeAnalyticsResponse(BaseModel):
    court_filter: Optional[str] = None
    jurisdiction_filter: Optional[str] = None
    status: str = "reserved_for_part_2"
    message: str
    total_analyzed: int = 0
    disposition_distribution: Dict[str, int] = {}
    average_case_duration_days: Optional[float] = None
    disclaimer: str = (
        "Historical disposition counts do not reflect current case merits or predict future court decisions."
    )

