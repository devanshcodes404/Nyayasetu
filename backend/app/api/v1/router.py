"""
API v1 Router aggregation.
Assembles all endpoint modules under /api/v1.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    auth,
    cases,
    documents,
    judgments,
    dataset,
    research,
    citations,
    analytics,
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(cases.router, prefix="/cases", tags=["Court Cases"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(judgments.router, prefix="/judgments", tags=["Public Judgments"])
api_router.include_router(dataset.router, prefix="/dataset", tags=["Dataset Pipeline"])
api_router.include_router(research.router, prefix="/research", tags=["Legal Research & RAG"])
api_router.include_router(citations.router, tags=["Citations"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics & Insights"])

