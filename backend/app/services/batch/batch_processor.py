import io
import json
import pandas as pd
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session

from app.models import Product, GeneratedContent, BatchJob, BatchItem
from app.schemas.product import ProductCreate
from app.schemas.brand_settings import BrandSettingsBase
from app.services.ai import AIService
from app.services.scoring.quality_scorer import QualityScorer

class BatchProcessor:
    @staticmethod
    def parse_file(file_bytes: bytes, file_type: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Parses uploaded file (CSV or JSON) into product dictionaries.
        Returns tuple of (valid_rows, invalid_rows_with_error_details).
        """
        valid_rows = []
        invalid_rows = []

        try:
            if file_type == "csv":
                df = pd.read_csv(io.BytesIO(file_bytes))
            elif file_type == "json":
                content = file_bytes.decode("utf-8")
                raw_json = json.loads(content)
                df = pd.DataFrame(raw_json if isinstance(raw_json, list) else [raw_json])
            else:
                raise ValueError("Unsupported file type. Use CSV or JSON.")
        except Exception as e:
            return [], [{"row_number": 0, "error": f"File parsing error: {str(e)}"}]

        # Standardize column mappings (e.g. productName -> name, productId -> sku)
        col_map = {
            "productName": "name",
            "productId": "sku",
            "targetAudience": "target_audience",
            "primaryKeywords": "primary_keywords",
            "secondaryKeywords": "secondary_keywords",
            "imageUrl": "image_url"
        }
        df.rename(columns=col_map, inplace=True)

        for index, row in df.iterrows():
            row_num = index + 1
            row_dict = row.to_dict()
            
            # Replace NaN with None
            cleaned_dict = {k: (None if pd.isna(v) else v) for k, v in row_dict.items()}
            
            # Validation
            name = cleaned_dict.get("name")
            category = cleaned_dict.get("category")

            if not name or str(name).strip() == "":
                invalid_rows.append({"row_number": row_num, "error": "Missing required field: 'productName' or 'name'."})
                continue
            if not category or str(category).strip() == "":
                invalid_rows.append({"row_number": row_num, "error": "Missing required field: 'category'."})
                continue

            # Parsing lists & dicts
            cleaned_dict["features"] = BatchProcessor._parse_list_field(cleaned_dict.get("features"))
            cleaned_dict["primary_keywords"] = BatchProcessor._parse_list_field(cleaned_dict.get("primary_keywords"))
            cleaned_dict["secondary_keywords"] = BatchProcessor._parse_list_field(cleaned_dict.get("secondary_keywords"))
            cleaned_dict["specifications"] = BatchProcessor._parse_dict_field(cleaned_dict.get("specifications"))
            
            # Ensure numeric price
            if cleaned_dict.get("price") is not None:
                try:
                    cleaned_dict["price"] = float(cleaned_dict["price"])
                except ValueError:
                    cleaned_dict["price"] = None

            cleaned_dict["row_number"] = row_num
            valid_rows.append(cleaned_dict)

        return valid_rows, invalid_rows

    @staticmethod
    def _parse_list_field(val: Any) -> List[str]:
        if not val or pd.isna(val):
            return []
        if isinstance(val, list):
            return [str(x).strip() for x in val if x]
        if isinstance(val, str):
            # Try parsing JSON string, or split by pipe/comma
            val_str = val.strip()
            if val_str.startswith("[") and val_str.endswith("]"):
                try:
                    return json.loads(val_str)
                except Exception:
                    pass
            return [x.strip() for x in val_str.replace("|", ",").split(",") if x.strip()]
        return []

    @staticmethod
    def _parse_dict_field(val: Any) -> Dict[str, Any]:
        if not val or pd.isna(val):
            return {}
        if isinstance(val, dict):
            return val
        if isinstance(val, str):
            val_str = val.strip()
            if val_str.startswith("{") and val_str.endswith("}"):
                try:
                    return json.loads(val_str)
                except Exception:
                    pass
            # Key-value string like "Key1: Val1, Key2: Val2"
            res = {}
            pairs = val_str.split(",")
            for p in pairs:
                if ":" in p:
                    k, v = p.split(":", 1)
                    res[k.strip()] = v.strip()
            return res
        return {}

    @staticmethod
    def process_batch(
        db: Session,
        batch_job: BatchJob,
        brand_settings: BrandSettingsBase,
        tone: str = "Professional",
        language: str = "English",
        word_count_preference: str = "Medium"
    ):
        """
        Executes generation for all pending items in a batch job.
        Updates job and item statuses in SQLite database.
        """
        batch_job.status = "processing"
        db.commit()

        items = db.query(BatchItem).filter(BatchItem.batch_job_id == batch_job.id).all()
        
        for item in items:
            if item.status in ["completed", "skipped"]:
                continue
            
            item.status = "processing"
            db.commit()
            
            try:
                product = db.query(Product).filter(Product.id == item.product_id).first()
                if not product:
                    item.status = "failed"
                    item.error_message = "Associated product record not found."
                    batch_job.failed_products += 1
                    batch_job.processed_products += 1
                    db.commit()
                    continue

                # Prepare schema for AI call
                prod_create = ProductCreate(
                    sku=product.sku,
                    name=product.name,
                    brand=product.brand,
                    category=product.category,
                    price=product.price,
                    currency=product.currency,
                    features=json.loads(product.features) if product.features else [],
                    specifications=json.loads(product.specifications) if product.specifications else {},
                    target_audience=product.target_audience,
                    primary_keywords=json.loads(product.primary_keywords) if product.primary_keywords else [],
                    secondary_keywords=json.loads(product.secondary_keywords) if product.secondary_keywords else [],
                    usp=product.usp,
                    image_url=product.image_url,
                    material=product.material,
                    dimensions=product.dimensions,
                    color=product.color,
                    weight=product.weight
                )

                # Call AI service (Dual AI Arbiter)
                content_dict, source, decision_meta = AIService.generate_description(
                    prod_create, brand_settings, tone, language, word_count_preference
                )

                # Calculate Scores
                scores = QualityScorer.calculate_scores(
                    prod_create,
                    content_dict["title"],
                    content_dict["short_description"],
                    content_dict["full_description"],
                    content_dict["meta_title"],
                    content_dict["meta_description"],
                    brand_settings,
                    tone
                )

                # Save GeneratedContent
                gen_content = GeneratedContent(
                    product_id=product.id,
                    title=content_dict["title"],
                    short_description=content_dict["short_description"],
                    full_description=content_dict["full_description"],
                    highlights=json.dumps(content_dict["highlights"]),
                    meta_title=content_dict["meta_title"],
                    meta_description=content_dict["meta_description"],
                    suggested_keywords=json.dumps(content_dict["suggested_keywords"]),
                    warnings=json.dumps(list(set(content_dict.get("warnings", []) + scores["recommendations"]))),
                    tone=tone,
                    language=language,
                    word_count_preference=word_count_preference,
                    seo_score=scores["seo_score"],
                    readability_score=scores["readability_score"],
                    completeness_score=scores["completeness_score"],
                    brand_tone_score=scores["brand_tone_score"],
                    quality_score=scores["quality_score"],
                    status="Draft",
                    generation_source=source,
                    candidates_data=json.dumps(decision_meta.get("candidates", [])),
                    decision_rationale=decision_meta.get("decision_rationale", "")
                )
                db.add(gen_content)
                db.flush()

                item.status = "completed"
                item.generated_content_id = gen_content.id
                batch_job.successful_products += 1
                batch_job.processed_products += 1

            except Exception as e:
                item.status = "failed"
                item.error_message = str(e)
                batch_job.failed_products += 1
                batch_job.processed_products += 1

            db.commit()

        batch_job.status = "completed"
        db.commit()
