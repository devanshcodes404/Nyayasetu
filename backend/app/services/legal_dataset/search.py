"""
Database-backed judgment search service.
Supports case title, parties, citations, CNR numbers, court, jurisdiction, date/year, and outcome filters.
Uses parameterized queries, database indexes, and pagination without requiring embeddings.
"""
from typing import Dict, Any, List, Optional
from sqlalchemy import or_, and_, desc
from sqlalchemy.orm import Session
from app.models.judgment import Judgment
from app.schemas.judgment import JudgmentSearchParams


class JudgmentSearchService:
    def __init__(self, db: Session):
        self.db = db

    def search(self, params: JudgmentSearchParams) -> Dict[str, Any]:
        """
        Executes parameterized database search across public Indian judgments.
        """
        query = self.db.query(Judgment)

        # General free-text keyword search
        if params.q and params.q.strip():
            term = f"%{params.q.strip()}%"
            query = query.filter(
                or_(
                    Judgment.title.ilike(term),
                    Judgment.party_caption.ilike(term),
                    Judgment.petitioner.ilike(term),
                    Judgment.respondent.ilike(term),
                    Judgment.docket_number.ilike(term),
                    Judgment.cnr_number.ilike(term),
                    Judgment.neutral_citation.ilike(term),
                    Judgment.law_report_citation.ilike(term),
                    Judgment.indexable_text.ilike(term),
                    Judgment.headnote_text.ilike(term),
                )
            )

        # Title specific filter
        if params.title and params.title.strip():
            query = query.filter(Judgment.title.ilike(f"%{params.title.strip()}%"))

        # Parties filter (petitioner or respondent)
        if params.party and params.party.strip():
            term = f"%{params.party.strip()}%"
            query = query.filter(
                or_(
                    Judgment.petitioner.ilike(term),
                    Judgment.respondent.ilike(term),
                    Judgment.party_caption.ilike(term),
                )
            )

        # Citation filter
        if params.citation and params.citation.strip():
            c_term = f"%{params.citation.strip()}%"
            query = query.filter(
                or_(
                    Judgment.neutral_citation.ilike(c_term),
                    Judgment.law_report_citation.ilike(c_term),
                )
            )

        # Docket or CNR
        if params.case_number and params.case_number.strip():
            query = query.filter(Judgment.docket_number.ilike(f"%{params.case_number.strip()}%"))
        if params.cnr_number and params.cnr_number.strip():
            query = query.filter(Judgment.cnr_number.ilike(f"%{params.cnr_number.strip()}%"))

        # Court & Jurisdiction filters
        if params.court and params.court.strip():
            query = query.filter(Judgment.court_name.ilike(f"%{params.court.strip()}%"))
        if params.jurisdiction and params.jurisdiction.strip():
            query = query.filter(Judgment.jurisdiction.ilike(f"%{params.jurisdiction.strip()}%"))

        # Year and Date Range filters
        if params.year:
            query = query.filter(Judgment.decision_year == params.year)
        if params.start_date:
            query = query.filter(Judgment.decision_date >= params.start_date)
        if params.end_date:
            query = query.filter(Judgment.decision_date <= params.end_date)

        # Disposition filter
        if params.disposition and params.disposition.strip():
            query = query.filter(
                or_(
                    Judgment.normalized_outcome.ilike(f"%{params.disposition.strip()}%"),
                    Judgment.disposition_text.ilike(f"%{params.disposition.strip()}%"),
                )
            )

        # Text availability filter
        if params.text_availability and params.text_availability.strip():
            query = query.filter(Judgment.text_availability_status == params.text_availability.strip())

        total = query.count()

        # Sort order: newest decision year/date first
        query = query.order_by(desc(Judgment.decision_date), desc(Judgment.id))

        # Pagination
        offset = (params.page - 1) * params.page_size
        items = query.offset(offset).limit(params.page_size).all()

        total_pages = (total + params.page_size - 1) // params.page_size if total > 0 else 1

        formatted_items = []
        for j in items:
            headnote_snip = j.headnote_text[:200] + "..." if j.headnote_text else None
            formatted_items.append({
                "id": j.id,
                "title": j.title,
                "petitioner": j.petitioner,
                "respondent": j.respondent,
                "party_caption": j.party_caption,
                "court_name": j.court_name,
                "docket_number": j.docket_number,
                "cnr_number": j.cnr_number,
                "neutral_citation": j.neutral_citation,
                "law_report_citation": j.law_report_citation,
                "decision_date": j.decision_date,
                "decision_year": j.decision_year,
                "disposition_text": j.disposition_text,
                "normalized_outcome": j.normalized_outcome,
                "text_availability_status": j.text_availability_status,
                "verification_status": j.verification_status,
                "has_source_pdf": bool(j.source_pdf_s3_url),
                "headnote_snippet": headnote_snip,
            })

        return {
            "items": formatted_items,
            "total": total,
            "page": params.page,
            "page_size": params.page_size,
            "total_pages": total_pages,
            "has_next": params.page < total_pages,
            "has_prev": params.page > 1,
        }

