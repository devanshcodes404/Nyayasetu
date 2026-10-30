"""
Judgment corpus endpoints: search, list, detail, and summary integration point.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.judgment import Judgment
from app.schemas.judgment import (
    JudgmentSearchParams,
    JudgmentDetailResponse,
)
from app.schemas.common import PaginatedResponse
from app.schemas.research import JudgmentSummaryResponse
from app.services.legal_dataset.search import JudgmentSearchService
from app.services.legal.summarizer import JudgmentSummarizerService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[dict])
def list_judgments(
    page: int = 1,
    page_size: int = 20,
    court: Optional[str] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db),
):
    params = JudgmentSearchParams(page=page, page_size=page_size, court=court, year=year)
    search_service = JudgmentSearchService(db)
    result = search_service.search(params)
    return PaginatedResponse(**result)


@router.get("/search", response_model=PaginatedResponse[dict])
def search_judgments(
    params: JudgmentSearchParams = Depends(),
    db: Session = Depends(get_db),
):
    search_service = JudgmentSearchService(db)
    result = search_service.search(params)
    return PaginatedResponse(**result)


@router.get("/{judgment_id}", response_model=JudgmentDetailResponse)
def get_judgment(
    judgment_id: int,
    db: Session = Depends(get_db),
):
    judgment = db.query(Judgment).filter(Judgment.id == judgment_id).first()
    if not judgment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Judgment with ID {judgment_id} not found in the public Indian case law corpus.",
        )
    return JudgmentDetailResponse.model_validate(judgment)


@router.get("/{judgment_id}/summary", response_model=JudgmentSummaryResponse)
def get_judgment_summary(
    judgment_id: int,
    db: Session = Depends(get_db),
):
    judgment = db.query(Judgment).filter(Judgment.id == judgment_id).first()
    if not judgment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Judgment with ID {judgment_id} not found.",
        )
    summarizer = JudgmentSummarizerService(db)
    return summarizer.summarize_judgment(judgment)

