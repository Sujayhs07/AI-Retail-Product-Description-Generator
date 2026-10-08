from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.schemas.product import ProductCreate

class GenerateDescriptionRequest(BaseModel):
    product: ProductCreate
    tone: str = Field(default="Professional", description="Selected content tone")
    language: str = Field(default="English", description="Target language")
    word_count_preference: str = Field(default="Medium", description="Short, Medium, Long")
    save_to_catalog: bool = Field(default=True, description="Save product and output to database")
    engine: str = Field(default="dual", description="Engine mode: 'dual' (Anthropic + Gemini decision), 'anthropic', or 'gemini'")

class RegenerateDescriptionRequest(BaseModel):
    product_id: int
    content_id: int
    tone: Optional[str] = "Professional"
    language: Optional[str] = "English"
    word_count_preference: Optional[str] = "Medium"
    engine: Optional[str] = "dual"

class ClaudeStructuredOutput(BaseModel):
    title: str
    short_description: str
    full_description: str
    highlights: List[str]
    meta_title: str
    meta_description: str
    suggested_keywords: List[str]
    warnings: List[str]

ProductDescriptionOutput = ClaudeStructuredOutput
