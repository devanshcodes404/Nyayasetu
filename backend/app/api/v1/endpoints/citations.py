"""
Citation extraction and verification endpoints.
Handles GET /api/v1/documents/{document_id}/citations.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.document import LegalDocument
from app.models.user import User
from app.schemas.research import CitationExtractionResponse
from app.api.v1.dependencies import get_current_user
from app.services.legal.citation_extractor import CitationExtractorService

router = APIRouter()


@router.get("/documents/{document_id}/citations", response_model=CitationExtractionResponse)
def get_document_citations(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = db.query(LegalDocument).filter(
        LegalDocument.id == document_id,
        LegalDocument.owner_id == current_user.id,
    ).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    extractor = CitationExtractorService(db)
    # Scan document text if available
    return extractor.extract_from_document(doc, text_content=doc.title)

