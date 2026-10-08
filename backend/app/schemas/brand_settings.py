from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class BrandSettingsBase(BaseModel):
    brand_name: str = "CatalogCraft Retail"
    brand_voice: str = "Professional, customer-focused, articulate, and accurate."
    preferred_words: List[str] = ["innovative", "premium", "sustainable", "durable"]
    prohibited_words: List[str] = ["cheap", "best in class", "guaranteed #1", "world's finest"]
    mandatory_disclaimer: Optional[str] = "Specifications subject to minor variations by manufacturing batch."
    content_rules: Optional[str] = "Always emphasize customer benefits before technical specifications."
    default_tone: str = "Professional"
    default_language: str = "English"
    default_word_count: str = "Medium"
    keyword_policy: str = "Natural placement, avoid keyword stuffing."
    allow_promotional_claims: bool = False
    max_keywords: int = 5
    include_feature_bullets: bool = True

class BrandSettingsUpdate(BrandSettingsBase):
    pass

class BrandSettingsResponse(BrandSettingsBase):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True
