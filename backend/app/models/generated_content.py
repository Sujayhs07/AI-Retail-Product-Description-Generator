import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class GeneratedContent(Base):
    __tablename__ = "generated_contents"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    
    title = Column(String, nullable=False)
    short_description = Column(Text, nullable=False)
    full_description = Column(Text, nullable=False)
    highlights = Column(Text, nullable=True)  # JSON list
    meta_title = Column(String, nullable=True)
    meta_description = Column(Text, nullable=True)
    suggested_keywords = Column(Text, nullable=True)  # JSON list
    warnings = Column(Text, nullable=True)  # JSON list
    
    tone = Column(String, default="Professional")
    language = Column(String, default="English")
    word_count_preference = Column(String, default="Medium")
    
    seo_score = Column(Float, default=0.0)
    readability_score = Column(Float, default=0.0)
    completeness_score = Column(Float, default=0.0)
    brand_tone_score = Column(Float, default=0.0)
    quality_score = Column(Float, default=0.0)
    
    status = Column(String, default="Draft")  # Draft, Approved, Needs Review
    generation_source = Column(String, default="mock")  # claude, gemini, dual_anthropic, dual_gemini, mock
    is_human_edited = Column(Boolean, default=False)
    candidates_data = Column(Text, nullable=True)  # JSON list of candidates
    decision_rationale = Column(Text, nullable=True)  # Explanation of decided perfect description
    
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    product = relationship("Product", back_populates="generated_contents")
    versions = relationship("ContentVersion", back_populates="generated_content", cascade="all, delete-orphan")


class ContentVersion(Base):
    __tablename__ = "content_versions"

    id = Column(Integer, primary_key=True, index=True)
    generated_content_id = Column(Integer, ForeignKey("generated_contents.id"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    content_snapshot = Column(Text, nullable=False)  # JSON dict of content fields
    changed_by = Column(String, default="System")
    change_type = Column(String, default="Generated")  # Generated, Human Edit, Regenerated
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    generated_content = relationship("GeneratedContent", back_populates="versions")
