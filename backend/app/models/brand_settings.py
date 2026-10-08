import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from app.database import Base

class BrandSettings(Base):
    __tablename__ = "brand_settings"

    id = Column(Integer, primary_key=True, index=True)
    brand_name = Column(String, default="CatalogCraft Retail")
    brand_voice = Column(Text, default="Professional, customer-focused, articulate, and accurate.")
    preferred_words = Column(Text, nullable=True)  # JSON list
    prohibited_words = Column(Text, nullable=True)  # JSON list
    mandatory_disclaimer = Column(Text, nullable=True)
    content_rules = Column(Text, nullable=True)
    default_tone = Column(String, default="Professional")
    default_language = Column(String, default="English")
    default_word_count = Column(String, default="Medium")
    keyword_policy = Column(String, default="Natural placement, avoid keyword stuffing.")
    allow_promotional_claims = Column(Boolean, default=False)
    max_keywords = Column(Integer, default=5)
    include_feature_bullets = Column(Boolean, default=True)
    
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
