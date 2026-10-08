from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ProductBase(BaseModel):
    sku: Optional[str] = None
    name: str = Field(..., description="Product name")
    brand: Optional[str] = None
    category: str = Field(..., description="Category name")
    price: Optional[float] = None
    currency: Optional[str] = "USD"
    features: Optional[List[str]] = []
    specifications: Optional[Dict[str, Any]] = {}
    target_audience: Optional[str] = None
    primary_keywords: Optional[List[str]] = []
    secondary_keywords: Optional[List[str]] = []
    usp: Optional[str] = None
    image_url: Optional[str] = None
    material: Optional[str] = None
    dimensions: Optional[str] = None
    color: Optional[str] = None
    weight: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    sku: Optional[str] = None
    name: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    features: Optional[List[str]] = None
    specifications: Optional[Dict[str, Any]] = None
    target_audience: Optional[str] = None
    primary_keywords: Optional[List[str]] = None
    secondary_keywords: Optional[List[str]] = None
    usp: Optional[str] = None
    image_url: Optional[str] = None
    material: Optional[str] = None
    dimensions: Optional[str] = None
    color: Optional[str] = None
    weight: Optional[str] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
