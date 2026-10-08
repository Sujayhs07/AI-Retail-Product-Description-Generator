import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product, GeneratedContent
from app.repositories import ProductRepository, ContentRepository, SettingsRepository
from app.schemas.generation import GenerateDescriptionRequest, RegenerateDescriptionRequest
from app.schemas.generated_content import GeneratedContentUpdate, GeneratedContentResponse
from app.services.ai import AIService
from app.services.scoring.quality_scorer import QualityScorer

router = APIRouter(prefix="/api", tags=["Generation"])

@router.post("/generate-description")
def generate_description(req: GenerateDescriptionRequest, db: Session = Depends(get_db)):
    # 1. Fetch brand settings
    brand_settings_db = SettingsRepository.get_settings(db)
    brand_settings = SettingsRepository.to_schema(brand_settings_db)

    # 2. Call AI Service (Claude + Gemini Dual Arbiter or selected engine)
    content_dict, source, decision_meta = AIService.generate_description(
        product=req.product,
        brand_settings=brand_settings,
        tone=req.tone,
        language=req.language,
        word_count_preference=req.word_count_preference,
        engine=req.engine or "dual"
    )

    # 3. Calculate Scores
    scores = QualityScorer.calculate_scores(
        product=req.product,
        title=content_dict["title"],
        short_desc=content_dict["short_description"],
        full_desc=content_dict["full_description"],
        meta_title=content_dict["meta_title"],
        meta_desc=content_dict["meta_description"],
        brand_settings=brand_settings,
        tone=req.tone
    )

    # Combine warnings & quality recommendations
    all_warnings = list(set(content_dict.get("warnings", []) + scores["recommendations"]))

    saved_product_id = None
    saved_content_id = None

    if req.save_to_catalog:
        # Create or update product in DB
        db_product = ProductRepository.create(db, req.product)
        saved_product_id = db_product.id

        # Check if GeneratedContent already exists for this product
        existing_content = db.query(GeneratedContent).filter(GeneratedContent.product_id == db_product.id).first()
        if existing_content:
            existing_content.title = content_dict["title"]
            existing_content.short_description = content_dict["short_description"]
            existing_content.full_description = content_dict["full_description"]
            existing_content.highlights = json.dumps(content_dict["highlights"])
            existing_content.meta_title = content_dict["meta_title"]
            existing_content.meta_description = content_dict["meta_description"]
            existing_content.suggested_keywords = json.dumps(content_dict["suggested_keywords"])
            existing_content.warnings = json.dumps(all_warnings)
            existing_content.tone = req.tone
            existing_content.language = req.language
            existing_content.word_count_preference = req.word_count_preference
            existing_content.seo_score = scores["seo_score"]
            existing_content.readability_score = scores["readability_score"]
            existing_content.completeness_score = scores["completeness_score"]
            existing_content.brand_tone_score = scores["brand_tone_score"]
            existing_content.quality_score = scores["quality_score"]
            existing_content.status = "Draft"
            existing_content.generation_source = source
            existing_content.candidates_data = json.dumps(decision_meta.get("candidates", []))
            existing_content.decision_rationale = decision_meta.get("decision_rationale", "")
            db.commit()
            db.refresh(existing_content)
            saved_content_id = existing_content.id
        else:
            gen_content = GeneratedContent(
                product_id=db_product.id,
                title=content_dict["title"],
                short_description=content_dict["short_description"],
                full_description=content_dict["full_description"],
                highlights=json.dumps(content_dict["highlights"]),
                meta_title=content_dict["meta_title"],
                meta_description=content_dict["meta_description"],
                suggested_keywords=json.dumps(content_dict["suggested_keywords"]),
                warnings=json.dumps(all_warnings),
                tone=req.tone,
                language=req.language,
                word_count_preference=req.word_count_preference,
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
            db.commit()
            db.refresh(gen_content)
            saved_content_id = gen_content.id

    return {
        "generated_content": {
            "id": saved_content_id,
            "product_id": saved_product_id,
            "title": content_dict["title"],
            "short_description": content_dict["short_description"],
            "full_description": content_dict["full_description"],
            "highlights": content_dict["highlights"],
            "meta_title": content_dict["meta_title"],
            "meta_description": content_dict["meta_description"],
            "suggested_keywords": content_dict["suggested_keywords"],
            "warnings": all_warnings,
            "tone": req.tone,
            "language": req.language,
            "word_count_preference": req.word_count_preference,
            "generation_source": source,
            "status": "Draft",
            "scores": scores,
            "candidates_data": decision_meta.get("candidates", []),
            "decision_rationale": decision_meta.get("decision_rationale", ""),
            "decision_summary": decision_meta
        }
    }

@router.post("/regenerate-description")
def regenerate_description(req: RegenerateDescriptionRequest, db: Session = Depends(get_db)):
    product = ProductRepository.get_by_id(db, req.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    content = ContentRepository.get_by_id(db, req.content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Generated content record not found")

    brand_settings_db = SettingsRepository.get_settings(db)
    brand_settings = SettingsRepository.to_schema(brand_settings_db)

    prod_schema = ProductRepository.to_dict(product)
    from app.schemas.product import ProductCreate
    prod_create = ProductCreate(**prod_schema)

    tone = req.tone or content.tone
    language = req.language or content.language
    word_count = req.word_count_preference or content.word_count_preference
    engine = req.engine or "dual"

    content_dict, source, decision_meta = AIService.generate_description(
        product=prod_create,
        brand_settings=brand_settings,
        tone=tone,
        language=language,
        word_count_preference=word_count,
        engine=engine
    )

    scores = QualityScorer.calculate_scores(
        product=prod_create,
        title=content_dict["title"],
        short_desc=content_dict["short_description"],
        full_desc=content_dict["full_description"],
        meta_title=content_dict["meta_title"],
        meta_desc=content_dict["meta_description"],
        brand_settings=brand_settings,
        tone=tone
    )

    all_warnings = list(set(content_dict.get("warnings", []) + scores["recommendations"]))

    update_dict = {
        "title": content_dict["title"],
        "short_description": content_dict["short_description"],
        "full_description": content_dict["full_description"],
        "highlights": content_dict["highlights"],
        "meta_title": content_dict["meta_title"],
        "meta_description": content_dict["meta_description"],
        "suggested_keywords": content_dict["suggested_keywords"],
        "warnings": all_warnings,
        "tone": tone,
        "language": language,
        "word_count_preference": word_count,
        "seo_score": scores["seo_score"],
        "readability_score": scores["readability_score"],
        "completeness_score": scores["completeness_score"],
        "brand_tone_score": scores["brand_tone_score"],
        "quality_score": scores["quality_score"],
        "generation_source": source,
        "candidates_data": json.dumps(decision_meta.get("candidates", [])),
        "decision_rationale": decision_meta.get("decision_rationale", ""),
        "status": "Draft"
    }

    updated_content = ContentRepository.update(db, content, update_dict, is_human=False)
    return ProductRepository.content_to_dict(updated_content)

@router.put("/generated-content/{content_id}")
def update_generated_content(content_id: int, req: GeneratedContentUpdate, db: Session = Depends(get_db)):
    content = ContentRepository.get_by_id(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Generated content record not found")

    update_dict = req.model_dump(exclude_unset=True)
    updated = ContentRepository.update(db, content, update_dict, is_human=True)
    return ProductRepository.content_to_dict(updated)

@router.post("/generated-content/{content_id}/approve")
def approve_content(content_id: int, db: Session = Depends(get_db)):
    content = ContentRepository.get_by_id(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Generated content record not found")

    updated = ContentRepository.update_status(db, content, "Approved")
    return ProductRepository.content_to_dict(updated)

@router.post("/generated-content/{content_id}/needs-review")
def mark_needs_review(content_id: int, db: Session = Depends(get_db)):
    content = ContentRepository.get_by_id(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Generated content record not found")

    updated = ContentRepository.update_status(db, content, "Needs Review")
    return ProductRepository.content_to_dict(updated)

@router.get("/generated-content/{content_id}/history")
def get_content_history(content_id: int, db: Session = Depends(get_db)):
    history = ContentRepository.get_history(db, content_id)
    return {"history": history}
