"""
Outcome insights and dashboard analytics endpoints.
"""
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.case import LegalCase
from app.models.document import LegalDocument
from app.models.judgment import Judgment
from app.models.user import User
from app.schemas.research import OutcomeAnalyticsResponse
from app.schemas.analytics import DashboardMetricsResponse
from app.api.v1.dependencies import get_current_user_optional
from app.services.legal.outcome_insights import OutcomeInsightsService

router = APIRouter()


@router.get("/outcomes", response_model=OutcomeAnalyticsResponse)
def get_outcome_analytics(
    court: Optional[str] = None,
    db: Session = Depends(get_db),
):
    service = OutcomeInsightsService(db)
    return service.get_outcome_insights(court_filter=court)


@router.get("/dashboard", response_model=DashboardMetricsResponse)
def get_dashboard_metrics(
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    my_cases_count = 0
    my_docs_count = 0
    recent_cases_list = []
    upcoming_hearings_list = []

    if current_user:
        my_cases_count = db.query(func.count(LegalCase.id)).filter(
            LegalCase.owner_id == current_user.id,
            LegalCase.status == "Active",
        ).scalar() or 0

        my_docs_count = db.query(func.count(LegalDocument.id)).filter(
            LegalDocument.owner_id == current_user.id,
        ).scalar() or 0

        cases = (
            db.query(LegalCase)
            .filter(LegalCase.owner_id == current_user.id)
            .order_by(LegalCase.updated_at.desc())
            .limit(5)
            .all()
        )
        for c in cases:
            recent_cases_list.append({
                "id": c.id,
                "title": c.title,
                "case_number": c.case_number,
                "court": c.court,
                "status": c.status,
                "next_hearing_date": str(c.next_hearing_date) if c.next_hearing_date else None,
            })

        hearings = (
            db.query(LegalCase)
            .filter(
                LegalCase.owner_id == current_user.id,
                LegalCase.next_hearing_date.isnot(None),
            )
            .order_by(LegalCase.next_hearing_date.asc())
            .limit(5)
            .all()
        )
        for h in hearings:
            upcoming_hearings_list.append({
                "case_id": h.id,
                "title": h.title,
                "case_number": h.case_number,
                "court": h.court,
                "date": str(h.next_hearing_date),
            })

    # Public corpus statistics
    public_total = db.query(func.count(Judgment.id)).scalar() or 0
    searchable = db.query(func.count(Judgment.id)).filter(
        Judgment.text_availability_status.in_(["FullText", "ShortIndexable", "HeadnoteOnly"])
    ).scalar() or 0
    courts_count = db.query(func.count(func.distinct(Judgment.court_name))).scalar() or 0

    return DashboardMetricsResponse(
        my_active_cases=my_cases_count,
        my_total_documents=my_docs_count,
        my_upcoming_hearings_count=len(upcoming_hearings_list),
        public_judgments_imported=public_total,
        public_judgments_searchable=searchable,
        public_courts_count=courts_count,
        recent_cases=recent_cases_list,
        upcoming_hearings=upcoming_hearings_list,
    )

