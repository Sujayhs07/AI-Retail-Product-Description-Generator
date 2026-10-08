from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("")
def list_products(
    search: Optional[str] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    tone: Optional[str] = None,
    min_quality_score: Optional[float] = None,
    min_seo_score: Optional[float] = None,
    sort_by: str = "newest",
    page: int = 1,
    page_size: int = 12,
    db: Session = Depends(get_db)
):
    items, total = ProductRepository.get_all(
        db,
        search=search,
        category=category,
        brand=brand,
        status=status_filter,
        tone=tone,
        min_quality_score=min_quality_score,
        min_seo_score=min_seo_score,
        sort_by=sort_by,
        page=page,
        page_size=page_size
    )
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size if page_size > 0 else 1
    }

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    db_product = ProductRepository.create(db, product_in)
    return ProductRepository.to_dict(db_product)

@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = ProductRepository.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Attach generated content if exists
    from app.repositories import ContentRepository
    content = ContentRepository.get_by_product_id(db, product_id)
    
    return {
        "product": ProductRepository.to_dict(product),
        "generated_content": ProductRepository.content_to_dict(content) if content else None
    }

@router.put("/{product_id}")
def update_product(product_id: int, product_in: ProductUpdate, db: Session = Depends(get_db)):
    product = ProductRepository.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    updated = ProductRepository.update(db, product, product_in)
    return ProductRepository.to_dict(updated)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = ProductRepository.delete(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
