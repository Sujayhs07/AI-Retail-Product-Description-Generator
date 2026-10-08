import json
import logging
from typing import Dict, Any, Tuple
import anthropic

from app.config import settings
from app.schemas.product import ProductCreate
from app.schemas.brand_settings import BrandSettingsBase
from app.schemas.generation import ProductDescriptionOutput
from app.services.ai.prompt_builder import PromptBuilder
from app.services.ai.mock_generator import MockGenerator

logger = logging.getLogger(__name__)

class AnthropicGenerator:
    @staticmethod
    def generate(
        product: ProductCreate,
        brand_settings: BrandSettingsBase,
        tone: str = "Professional",
        language: str = "English",
        word_count_preference: str = "Medium"
    ) -> Tuple[Dict[str, Any], str]:
        """
        Generates product description using Anthropic Claude API.
        Falls back to MockGenerator (Claude style) if key is missing or on error.
        Returns tuple of (content_dict, generation_source).
        """
        api_key = settings.ANTHROPIC_API_KEY.strip() if settings.ANTHROPIC_API_KEY else ""

        if not api_key:
            logger.info("No ANTHROPIC_API_KEY configured. Using Claude-style MockGenerator.")
            mock_data = MockGenerator.generate(product, brand_settings, tone, language, word_count_preference, provider="claude")
            return mock_data, "mock"

        try:
            logger.info(f"Invoking Anthropic Claude API with model {settings.CLAUDE_MODEL}...")
            client = anthropic.Anthropic(api_key=api_key)

            system_prompt = PromptBuilder.build_system_prompt(brand_settings)
            user_prompt = PromptBuilder.build_user_prompt(product, tone, language, word_count_preference)

            response = client.messages.create(
                model=settings.CLAUDE_MODEL,
                max_tokens=1500,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            response_text = response.content[0].text.strip()

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
            return validated.model_dump(), "claude"

        except Exception as e:
            logger.error(f"Anthropic Claude API call failed: {str(e)}. Falling back to MockGenerator.")
            mock_data = MockGenerator.generate(product, brand_settings, tone, language, word_count_preference, provider="claude")
            mock_data["warnings"].append(f"Anthropic API Notice: ({type(e).__name__}); generated via Mock Engine.")
            return mock_data, "mock"
