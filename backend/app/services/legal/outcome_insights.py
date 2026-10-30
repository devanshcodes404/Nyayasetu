"""
Case Outcome Analytics Service (Part 2 interface).
Provides statistical distributions over historical dispositions.
Strictly disclaims predictive guarantees.
"""
from typing import Dict, Any, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.judgment import Judgment
from app.schemas.research import OutcomeAnalyticsResponse


class OutcomeInsightsService:
    def __init__(self, db: Session):
        self.db = db

    def get_outcome_insights(self, court_filter: Optional[str] = None) -> OutcomeAnalyticsResponse:
        """
        Aggregates historical dispositions.
        """
        query = self.db.query(Judgment.normalized_outcome, func.count(Judgment.id))
        if court_filter:
            query = query.filter(Judgment.court_name.ilike(f"%{court_filter}%"))
        
        query = query.filter(Judgment.normalized_outcome.isnot(None)).group_by(Judgment.normalized_outcome)
        results = query.all()
        
        distribution = {outcome: count for outcome, count in results if outcome}
        total = sum(distribution.values())

        return OutcomeAnalyticsResponse(
            court_filter=court_filter,
            status="foundation_active",
            message="Outcome insights calculated from imported public judgment records.",
            total_analyzed=total,
            disposition_distribution=distribution,
            disclaimer=(
                "Historical disposition trends are informational only and do NOT predict future judicial outcomes "
                "or substitute for legal counsel."
            ),
        )

