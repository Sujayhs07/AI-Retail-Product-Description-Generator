from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class DashboardMetrics(BaseModel):
    total_products: int
    descriptions_generated: int
    approved_descriptions: int
    products_needing_review: int
    avg_seo_score: float
    avg_quality_score: float
    batch_jobs_completed: int

class ActivityLog(BaseModel):
    id: int
    product_name: str
    action: str
    status: str
    score: float
    timestamp: str
    source: str

class AnalyticsOverview(BaseModel):
    metrics: DashboardMetrics
    generations_over_time: List[Dict[str, Any]]
    products_by_category: List[Dict[str, Any]]
    quality_score_distribution: List[Dict[str, Any]]
    seo_score_distribution: List[Dict[str, Any]]
    tone_usage: List[Dict[str, Any]]
    status_distribution: List[Dict[str, Any]]
    recent_activities: List[ActivityLog]
