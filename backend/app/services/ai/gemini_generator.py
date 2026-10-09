import json
import logging
from typing import Dict, Any, Tuple
from google import genai
from google.genai import types

from app.config import settings
from app.schemas.product import ProductCreate
from app.schemas.brand_settings import BrandSettingsBase
from app.schemas.generation import ProductDescriptionOutput
from app.services.ai.prompt_builder import PromptBuilder
from app.services.ai.mock_generator import MockGenerator

logger = logging.getLogger(__name__)

class GeminiGenerator:
    @staticmethod
    def _normalize_model_name(raw_model: str) -> str:
        clean = (raw_model or "gemini-2.5-flash-lite").strip().lower()
        if "3.5" in clean:
            # Normalize 'gemini 3.5 lite' to modern Google GenAI flash-lite target
            return "gemini-2.5-flash-lite"
        return clean.replace(" ", "-")

    @staticmethod
    def generate(
        product: ProductCreate,
        brand_settings: BrandSettingsBase,
        tone: str = "Professional",
        language: str = "English",
        word_count_preference: str = "Medium"
    ) -> Tuple[Dict[str, Any], str]:
        """
        Generates product description using Google Gemini API (Gemini 3.5 / 2.5 Flash Lite).
        Falls back to MockGenerator (Gemini style) if key is missing or on error.
        Returns tuple of (content_dict, generation_source).
        """
        api_key = settings.GEMINI_API_KEY.strip() if settings.GEMINI_API_KEY else ""

        if not api_key:
            logger.info("No GEMINI_API_KEY configured. Using Gemini-style MockGenerator.")
            mock_data = MockGenerator.generate(
                product, brand_settings, tone, language, word_count_preference, provider="gemini"
            )
            mock_data.setdefault("warnings", []).append("API Key Notice: GEMINI_API_KEY is empty. Switched to offline Deterministic Mock Generator.")
            return mock_data, "mock"

        if api_key.startswith("sk-"):
            logger.warning("Configured GEMINI_API_KEY appears to be an OpenAI key (starts with 'sk-'). Google Gemini keys start with 'AIzaSy'. Falling back to Gemini mock engine.")
            mock_data = MockGenerator.generate(
                product, brand_settings, tone, language, word_count_preference, provider="gemini"
            )
            mock_data["warnings"].append("Key Format Notice: GEMINI_API_KEY in .env starts with 'sk-' (OpenAI format). Google Gemini keys start with 'AIzaSy' from Google AI Studio (aistudio.google.com). Generated via Gemini mock engine.")
            return mock_data, "mock"

        model_name = GeminiGenerator._normalize_model_name(settings.GEMINI_MODEL)

        try:
            logger.info(f"Invoking Google Gemini API with model '{model_name}'...")
            client = genai.Client(api_key=api_key)

            system_prompt = PromptBuilder.build_system_prompt(brand_settings)
            user_prompt = PromptBuilder.build_user_prompt(product, tone, language, word_count_preference)

            # Try primary target model with fallback cascade if specific model ID differs on API
            models_to_try = [model_name, "gemini-2.5-flash-lite", "gemini-2.0-flash", "gemini-1.5-flash"]
            # Deduplicate maintaining order
            models_to_try = list(dict.fromkeys(models_to_try))

            response = None
            last_err = None

            for m in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=m,
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            response_mime_type="application/json",
                            temperature=0.7,
                        )
                    )
                    if response and response.text:
                        break
                except Exception as ex:
                    last_err = ex
                    err_msg = str(ex).lower()
                    if "api_key_invalid" in err_msg or "api key not valid" in err_msg:
                        logger.warning("Gemini API key is invalid. Aborting further model cascades.")
                        break
                    logger.warning(f"Gemini model '{m}' call failed: {str(ex)}. Trying next fallback...")
                    continue

            if not response or not response.text:
                raise last_err or RuntimeError("No response returned from Gemini API")

            response_text = response.text.strip()

            # Clean markdown code block wraps if present
            if response_text.startswith("```"):
                lines = response_text.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                response_text = "\n".join(lines).strip()

            parsed_json = json.loads(response_text)
            validated = ProductDescriptionOutput(**parsed_json)
            return validated.model_dump(), "gemini"

        except Exception as e:
            logger.error(f"Google Gemini API call failed: {str(e)}. Falling back to MockGenerator.")
            mock_data = MockGenerator.generate(
                product, brand_settings, tone, language, word_count_preference, provider="gemini"
            )
            mock_data["warnings"].append(f"Gemini API Notice: ({type(e).__name__}); generated via Mock Engine.")
            return mock_data, "mock"
