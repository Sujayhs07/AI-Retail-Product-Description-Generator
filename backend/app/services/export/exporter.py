import json
import pandas as pd
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models import Product, GeneratedContent

class ContentExporter:
    @staticmethod
    def prepare_export_data(db: Session, batch_job_id: int = None) -> List[Dict[str, Any]]:
        query = db.query(Product, GeneratedContent).outerjoin(
            GeneratedContent, Product.id == GeneratedContent.product_id
        )

        data = []
        for prod, content in query.all():
            row = {
                "product_id": prod.id,
                "sku": prod.sku,
                "product_name": prod.name,
                "brand": prod.brand,
                "category": prod.category,
                "price": prod.price,
                "currency": prod.currency,
                "features": prod.features,
                "target_audience": prod.target_audience,
                "primary_keywords": prod.primary_keywords,
                "generated_title": content.title if content else "",
                "short_description": content.short_description if content else "",
                "full_description": content.full_description if content else "",
                "highlights": content.highlights if content else "[]",
                "meta_title": content.meta_title if content else "",
                "meta_description": content.meta_description if content else "",
                "suggested_keywords": content.suggested_keywords if content else "[]",
                "quality_score": content.quality_score if content else 0.0,
                "seo_score": content.seo_score if content else 0.0,
                "status": content.status if content else "Not Generated",
                "generation_source": content.generation_source if content else ""
            }
            data.append(row)
        return data

    @staticmethod
    def to_csv_string(data: List[Dict[str, Any]]) -> str:
        df = pd.DataFrame(data)
        return df.to_csv(index=False)

    @staticmethod
    def to_json_string(data: List[Dict[str, Any]]) -> str:
        # Parse JSON fields inside rows for clean output
        clean_data = []
        for item in data:
            row = dict(item)
            for k in ["features", "primary_keywords", "highlights", "suggested_keywords"]:
                if isinstance(row.get(k), str):
                    try:
                        row[k] = json.loads(row[k])
                    except Exception:
                        pass
            clean_data.append(row)
        return json.dumps(clean_data, indent=2)
