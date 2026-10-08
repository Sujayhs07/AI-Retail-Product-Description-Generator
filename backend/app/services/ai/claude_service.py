import logging
from typing import Dict, Any, Tuple
from app.schemas.product import ProductCreate
from app.schemas.brand_settings import BrandSettingsBase
from app.services.ai.description_decider import DescriptionDecider

logger = logging.getLogger(__name__)

class AIService:
    @staticmethod
    def generate_description(
        product: ProductCreate,
        brand_settings: BrandSettingsBase,
        tone: str = "Professional",
        language: str = "English",
        word_count_preference: str = "Medium",
        engine: str = "dual"
    ) -> Tuple[Dict[str, Any], str, Dict[str, Any]]:
        """
        Coordinates generation and decides the perfect description using Anthropic and Google Gemini.
        Returns tuple of (content_dict, generation_source, decision_metadata).
        """
        return DescriptionDecider.decide_perfect_description(
            product=product,
            brand_settings=brand_settings,
            tone=tone,
            language=language,
            word_count_preference=word_count_preference,
            engine_mode=engine
        )
