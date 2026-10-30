"""
Court Case management endpoints: list, create, retrieve, update, delete.
Enforces strict owner-level multi-tenancy.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.session import get_db
from app.models.case import LegalCase
from app.models.user import User
from app.schemas.case import CaseCreateRequest, CaseUpdateRequest, CaseResponse
from app.api.v1.dependencies import get_current_user

router = APIRouter()


@router.get("", response_model=List[CaseResponse])
def list_cases(
    status_filter: Optional[str] = Query(None, alias="status"),
    q: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(LegalCase).filter(LegalCase.owner_id == current_user.id)
    if status_filter:
        query = query.filter(LegalCase.status.ilike(status_filter))
    if q and q.strip():
        term = f"%{q.strip()}%"
        query = query.filter(
            LegalCase.title.ilike(term) |
            LegalCase.case_number.ilike(term) |
            LegalCase.court.ilike(term) |
            LegalCase.client_name.ilike(term)
        )
    cases = query.order_by(desc(LegalCase.created_at)).all()
    
    # Enrich with document counts
    results = []
    for c in cases:
        resp = CaseResponse.model_validate(c)
        resp.documents_count = len(c.documents) if c.documents else 0
        results.append(resp)
    return results


@router.post("", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
def create_case(
    request: CaseCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    case = LegalCase(
        owner_id=current_user.id,
        title=request.title.strip(),
        case_number=request.case_number.strip(),
        court=request.court.strip(),
        jurisdiction=request.jurisdiction.strip(),
        case_type=request.case_type.strip(),
        client_name=request.client_name.strip(),
        opposing_party=request.opposing_party.strip(),
        status=request.status.strip(),
        filing_date=request.filing_date,
        next_hearing_date=request.next_hearing_date,
        description=request.description,
    )
    db.add(case)
    db.commit()
    db.refresh(case)
    return CaseResponse.model_validate(case)


@router.get("/{case_id}", response_model=CaseResponse)
def get_case(
    case_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    case = db.query(LegalCase).filter(LegalCase.id == case_id, LegalCase.owner_id == current_user.id).first()
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found.")
    resp = CaseResponse.model_validate(case)
    resp.documents_count = len(case.documents) if case.documents else 0
    return resp


@router.patch("/{case_id}", response_model=CaseResponse)
def update_case(
    case_id: int,
    request: CaseUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    case = db.query(LegalCase).filter(LegalCase.id == case_id, LegalCase.owner_id == current_user.id).first()
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found.")

    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(case, field, value)

    db.commit()
    db.refresh(case)
    resp = CaseResponse.model_validate(case)
    resp.documents_count = len(case.documents) if case.documents else 0
    return resp


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_case(
    case_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    case = db.query(LegalCase).filter(LegalCase.id == case_id, LegalCase.owner_id == current_user.id).first()
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found.")

    db.delete(case)
    db.commit()
    return None

