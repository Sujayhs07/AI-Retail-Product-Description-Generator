from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class BatchItemResponse(BaseModel):
    id: int
    batch_job_id: int
    product_id: Optional[int] = None
    row_number: int
    status: str
    error_message: Optional[str] = None
    generated_content_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BatchJobResponse(BaseModel):
    id: int
    file_name: str
    file_type: str
    total_products: int
    processed_products: int
    successful_products: int
    failed_products: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    items: Optional[List[BatchItemResponse]] = []

    class Config:
        from_attributes = True

class BatchGenerateRequest(BaseModel):
    tone: Optional[str] = "Professional"
    language: Optional[str] = "English"
    word_count_preference: Optional[str] = "Medium"
    selected_product_ids: Optional[List[int]] = None
