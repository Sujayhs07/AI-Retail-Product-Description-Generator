import json
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models.brand_settings import BrandSettings
from app.schemas.brand_settings import BrandSettingsBase, BrandSettingsUpdate

class SettingsRepository:
    @staticmethod
    def get_settings(db: Session) -> BrandSettings:
        settings = db.query(BrandSettings).first()
        if not settings:
            # Seed default settings
            settings = BrandSettings(
                brand_name="CatalogCraft Retail",
                brand_voice="Professional, customer-focused, articulate, and accurate.",
                preferred_words=json.dumps(["innovative", "premium", "sustainable", "durable"]),
                prohibited_words=json.dumps(["cheap", "best in class", "guaranteed #1", "world's finest"]),
                mandatory_disclaimer="Specifications subject to minor variations by manufacturing batch.",
                content_rules="Always emphasize customer benefits before technical specifications.",
                default_tone="Professional",
                default_language="English",
                default_word_count="Medium",
                keyword_policy="Natural placement, avoid keyword stuffing.",
                allow_promotional_claims=False,
                max_keywords=5,
                include_feature_bullets=True
            )
            db.add(settings)
            db.commit()
            db.refresh(settings)
        return settings

    @staticmethod
    def update_settings(db: Session, settings_in: BrandSettingsUpdate) -> BrandSettings:
        settings = SettingsRepository.get_settings(db)
        update_data = settings_in.model_dump(exclude_unset=True)

        for k, v in update_data.items():
            if k in ["preferred_words", "prohibited_words"]:
                setattr(settings, k, json.dumps(v) if v is not None else None)
            else:
                setattr(settings, k, v)

        db.commit()
        db.refresh(settings)
        return settings

    @staticmethod
    def reset_to_defaults(db: Session) -> BrandSettings:
        settings = SettingsRepository.get_settings(db)
        settings.brand_name = "CatalogCraft Retail"
        settings.brand_voice = "Professional, customer-focused, articulate, and accurate."
        settings.preferred_words = json.dumps(["innovative", "premium", "sustainable", "durable"])
        settings.prohibited_words = json.dumps(["cheap", "best in class", "guaranteed #1", "world's finest"])
        settings.mandatory_disclaimer = "Specifications subject to minor variations by manufacturing batch."
        settings.content_rules = "Always emphasize customer benefits before technical specifications."
        settings.default_tone = "Professional"
        settings.default_language = "English"
        settings.default_word_count = "Medium"
        settings.keyword_policy = "Natural placement, avoid keyword stuffing."
        settings.allow_promotional_claims = False
        settings.max_keywords = 5
        settings.include_feature_bullets = True

        db.commit()
        db.refresh(settings)
        return settings

    @staticmethod
    def to_schema(settings: BrandSettings) -> BrandSettingsBase:
        return BrandSettingsBase(
            brand_name=settings.brand_name,
            brand_voice=settings.brand_voice,
            preferred_words=json.loads(settings.preferred_words) if settings.preferred_words else [],
            prohibited_words=json.loads(settings.prohibited_words) if settings.prohibited_words else [],
            mandatory_disclaimer=settings.mandatory_disclaimer,
            content_rules=settings.content_rules,
            default_tone=settings.default_tone,
            default_language=settings.default_language,
            default_word_count=settings.default_word_count,
            keyword_policy=settings.keyword_policy,
            allow_promotional_claims=settings.allow_promotional_claims,
            max_keywords=settings.max_keywords,
            include_feature_bullets=settings.include_feature_bullets
        )
