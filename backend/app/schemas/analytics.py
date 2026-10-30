"""
Analytics and dashboard metric schemas.
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class DashboardMetricsResponse(BaseModel):
    # Private user workspace statistics
    my_active_cases: int
    my_total_documents: int
    my_upcoming_hearings_count: int
    
    # Public Indian judgment corpus statistics
    public_judgments_imported: int
    public_judgments_searchable: int
    public_courts_count: int
    
    # Recent activity items
    recent_cases: List[Dict[str, Any]] = []
    upcoming_hearings: List[Dict[str, Any]] = []

