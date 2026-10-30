"""
Research endpoints (Part 2 AI readiness).
Handles POST /api/v1/research/ask and GET /api/v1/cases/{case_id}/similar.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.case import LegalCase
from app.models.user import User
from app.schemas.research import (
    ResearchQueryRequest,
    ResearchQueryResponse,
    SimilarCasesResponse,
)
from app.api.v1.dependencies import get_current_user
from app.services.legal.rag import LegalRAGService
from app.services.legal.similar_cases import SimilarCasesService

router = APIRouter()


@router.post("/ask", response_model=ResearchQueryResponse)
def ask_legal_research(
    request: ResearchQueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rag_service = LegalRAGService(db)
    return rag_service.query(request, user_id=current_user.id)


@router.get("/cases/{case_id}/similar", response_model=SimilarCasesResponse)
def get_similar_cases(
    case_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    case = db.query(LegalCase).filter(
        LegalCase.id == case_id,
        LegalCase.owner_id == current_user.id,
    ).first()
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found.")

    service = SimilarCasesService(db)
    return service.find_similar(case)

