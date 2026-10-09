from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class GeneratedContentBase(BaseModel):
    title: str
    short_description: str
    full_description: str
    highlights: List[str] = []
    meta_title: str
    meta_description: str
    suggested_keywords: List[str] = []
    warnings: List[str] = []

class GeneratedContentCreate(GeneratedContentBase):
    product_id: int
    tone: str = "Professional"
    language: str = "English"
    word_count_preference: str = "Medium"
    generation_source: str = "mock"

class GeneratedContentUpdate(BaseModel):
    title: Optional[str] = None
    short_description: Optional[str] = None
    full_description: Optional[str] = None
    highlights: Optional[List[str]] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    suggested_keywords: Optional[List[str]] = None
    warnings: Optional[List[str]] = None
    status: Optional[str] = None
    candidates_data: Optional[List[Dict[str, Any]]] = None
    decision_rationale: Optional[str] = None
    seo_score: Optional[float] = None
    readability_score: Optional[float] = None
    completeness_score: Optional[float] = None
    brand_tone_score: Optional[float] = None
    quality_score: Optional[float] = None
    generation_source: Optional[str] = None

class ContentVersionResponse(BaseModel):
    id: int
    generated_content_id: int
    version_number: int
    content_snapshot: Dict[str, Any]
    changed_by: str
    change_type: str
    created_at: datetime

    class Config:
        from_attributes = True

class GeneratedContentResponse(GeneratedContentBase):
    id: int
    product_id: int
    tone: str
    language: str
    word_count_preference: str
    seo_score: float
    readability_score: float
    completeness_score: float
    brand_tone_score: float
    quality_score: float
    status: str
    generation_source: str
    is_human_edited: bool
    candidates_data: Optional[List[Dict[str, Any]]] = []
    decision_rationale: Optional[str] = ""
    api_key_notice: Optional[Dict[str, Any]] = None
    generated_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

