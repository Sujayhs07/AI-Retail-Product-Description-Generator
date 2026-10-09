import json
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models import Product, GeneratedContent
from app.schemas.product import ProductCreate, ProductUpdate

class ProductRepository:
    @staticmethod
    def create(db: Session, product_in: ProductCreate) -> Product:
        # If product with same SKU exists, update its attributes rather than failing on unique constraint
        if product_in.sku:
            existing = db.query(Product).filter(Product.sku == product_in.sku).first()
            if existing:
                existing.name = product_in.name
                if product_in.brand:
                    existing.brand = product_in.brand
                existing.category = product_in.category
                if product_in.price is not None:
                    existing.price = product_in.price
                if product_in.currency:
                    existing.currency = product_in.currency
                if product_in.features is not None:
                    existing.features = json.dumps(product_in.features)
                if product_in.specifications is not None:
                    existing.specifications = json.dumps(product_in.specifications)
                if product_in.target_audience:
                    existing.target_audience = product_in.target_audience
                if product_in.primary_keywords is not None:
                    existing.primary_keywords = json.dumps(product_in.primary_keywords)
                if product_in.secondary_keywords is not None:
                    existing.secondary_keywords = json.dumps(product_in.secondary_keywords)
                if product_in.usp:
                    existing.usp = product_in.usp
                if product_in.image_url:
                    existing.image_url = product_in.image_url
                if product_in.material:
                    existing.material = product_in.material
                if product_in.dimensions:
                    existing.dimensions = product_in.dimensions
                if product_in.color:
                    existing.color = product_in.color
                if product_in.weight:
                    existing.weight = product_in.weight
                db.commit()
                db.refresh(existing)
                return existing

        db_product = Product(
            sku=product_in.sku,
            name=product_in.name,
            brand=product_in.brand,
            category=product_in.category,
            price=product_in.price,
            currency=product_in.currency or "USD",
            features=json.dumps(product_in.features or []),
            specifications=json.dumps(product_in.specifications or {}),
            target_audience=product_in.target_audience,
            primary_keywords=json.dumps(product_in.primary_keywords or []),
            secondary_keywords=json.dumps(product_in.secondary_keywords or []),
            usp=product_in.usp,
            image_url=product_in.image_url,
            material=product_in.material,
            dimensions=product_in.dimensions,
            color=product_in.color,
            weight=product_in.weight
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def get_by_id(db: Session, product_id: int) -> Optional[Product]:
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def get_all(
        db: Session,
        search: Optional[str] = None,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        status: Optional[str] = None,
        tone: Optional[str] = None,
        min_quality_score: Optional[float] = None,
        min_seo_score: Optional[float] = None,
        sort_by: str = "newest",
        page: int = 1,
        page_size: int = 12
    ) -> Tuple[List[Dict[str, Any]], int]:
        query = db.query(Product, GeneratedContent).outerjoin(
            GeneratedContent, Product.id == GeneratedContent.product_id
        )

        if search:
            pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Product.name.ilike(pattern),
                    Product.sku.ilike(pattern),
                    Product.brand.ilike(pattern),
                    Product.category.ilike(pattern)
                )
            )

        if category and category != "All":
            query = query.filter(Product.category == category)

        if brand and brand != "All":
            query = query.filter(Product.brand == brand)

        if status and status != "All":
            query = query.filter(GeneratedContent.status == status)

        if tone and tone != "All":
            query = query.filter(GeneratedContent.tone == tone)

        if min_quality_score is not None:
            query = query.filter(GeneratedContent.quality_score >= min_quality_score)

        if min_seo_score is not None:
            query = query.filter(GeneratedContent.seo_score >= min_seo_score)

        # Sorting
        if sort_by == "oldest":
            query = query.order_by(Product.created_at.asc())
        elif sort_by == "name":
            query = query.order_by(Product.name.asc())
        elif sort_by == "quality_score":
            query = query.order_by(GeneratedContent.quality_score.desc().nullslast())
        elif sort_by == "seo_score":
            query = query.order_by(GeneratedContent.seo_score.desc().nullslast())
        else:  # newest
            query = query.order_by(Product.created_at.desc())

        total = query.count()
        offset = (page - 1) * page_size
        results = query.offset(offset).limit(page_size).all()

        formatted_results = []
        for prod, content in results:
            item = {
                "product": ProductRepository.to_dict(prod),
                "generated_content": ProductRepository.content_to_dict(content) if content else None
            }
            formatted_results.append(item)

        return formatted_results, total

    @staticmethod
    def update(db: Session, product: Product, product_in: ProductUpdate) -> Product:
        update_data = product_in.model_dump(exclude_unset=True)
        
        for k, v in update_data.items():
            if k in ["features", "specifications", "primary_keywords", "secondary_keywords"]:
                setattr(product, k, json.dumps(v) if v is not None else None)
            else:
                setattr(product, k, v)

        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete(db: Session, product_id: int) -> bool:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return False
        db.delete(product)
        db.commit()
        return True

    @staticmethod
    def to_dict(product: Product) -> Dict[str, Any]:
        return {
            "id": product.id,
            "sku": product.sku,
            "name": product.name,
            "brand": product.brand,
            "category": product.category,
            "price": product.price,
            "currency": product.currency,
            "features": json.loads(product.features) if product.features else [],
            "specifications": json.loads(product.specifications) if product.specifications else {},
            "target_audience": product.target_audience,
            "primary_keywords": json.loads(product.primary_keywords) if product.primary_keywords else [],
            "secondary_keywords": json.loads(product.secondary_keywords) if product.secondary_keywords else [],
            "usp": product.usp,
            "image_url": product.image_url,
            "material": product.material,
            "dimensions": product.dimensions,
            "color": product.color,
            "weight": product.weight,
            "created_at": product.created_at.isoformat() if product.created_at else None,
            "updated_at": product.updated_at.isoformat() if product.updated_at else None,
        }

    @staticmethod
    def content_to_dict(content: GeneratedContent) -> Dict[str, Any]:
        candidates_raw = getattr(content, "candidates_data", None)
        if isinstance(candidates_raw, str) and candidates_raw.strip():
            try:
                candidates_parsed = json.loads(candidates_raw)
            except Exception:
                candidates_parsed = []
        elif isinstance(candidates_raw, list):
            candidates_parsed = candidates_raw
        else:
            candidates_parsed = []

        q_score = float(content.quality_score) if content.quality_score is not None else 0.0
        s_score = float(content.seo_score) if content.seo_score is not None else 0.0
        r_score = float(content.readability_score) if content.readability_score is not None else 0.0
        c_score = float(content.completeness_score) if content.completeness_score is not None else 0.0
        b_score = float(content.brand_tone_score) if content.brand_tone_score is not None else 0.0

        warnings_list = json.loads(content.warnings) if content.warnings else []

        return {
            "id": content.id,
            "product_id": content.product_id,
            "title": content.title,
            "short_description": content.short_description,
            "full_description": content.full_description,
            "highlights": json.loads(content.highlights) if content.highlights else [],
            "meta_title": content.meta_title,
            "meta_description": content.meta_description,
            "suggested_keywords": json.loads(content.suggested_keywords) if content.suggested_keywords else [],
            "warnings": warnings_list,
            "tone": content.tone,
            "language": content.language,
            "word_count_preference": content.word_count_preference,
            "seo_score": s_score,
            "readability_score": r_score,
            "completeness_score": c_score,
            "brand_tone_score": b_score,
            "quality_score": q_score,
            "scores": {
                "quality_score": q_score,
                "seo_score": s_score,
                "readability_score": r_score,
                "completeness_score": c_score,
                "brand_tone_score": b_score,
                "recommendations": warnings_list,
            },
            "status": content.status,
            "generation_source": content.generation_source,
            "is_human_edited": content.is_human_edited or False,
            "candidates_data": candidates_parsed,
            "decision_rationale": getattr(content, "decision_rationale", None) or "",
            "generated_at": content.generated_at.isoformat() if content.generated_at else None,
            "updated_at": content.updated_at.isoformat() if content.updated_at else None,
        }
