import logging
from typing import Dict, Any, Tuple, List
from app.config import settings
from app.schemas.product import ProductCreate
from app.schemas.brand_settings import BrandSettingsBase
from app.services.scoring.quality_scorer import QualityScorer
from app.services.ai.anthropic_generator import AnthropicGenerator
from app.services.ai.gemini_generator import GeminiGenerator

logger = logging.getLogger(__name__)

class DescriptionDecider:
    @staticmethod
    def decide_perfect_description(
        product: ProductCreate,
        brand_settings: BrandSettingsBase,
        tone: str = "Professional",
        language: str = "English",
        word_count_preference: str = "Medium",
        engine_mode: str = "dual"
    ) -> Tuple[Dict[str, Any], str, Dict[str, Any]]:
        """
        Coordinates generation between Anthropic Claude and Google Gemini (Gemini 3.5 / 2.5 Flash Lite),
        benchmarks both candidates across all retail and SEO dimensions,
        and decides the 'Perfect Description' with transparent comparative rationale.

        engine_mode:
            - 'dual': Generates with both Anthropic Claude and Google Gemini, arbitrates and decides the winner.
            - 'gemini': Generates directly with Google Gemini.
            - 'anthropic': Generates directly with Anthropic Claude.
        """
        engine_mode_clean = (engine_mode or "dual").lower().strip()

        if engine_mode_clean in ["gemini", "google"]:
            content, source = GeminiGenerator.generate(
                product, brand_settings, tone, language, word_count_preference
            )
            scores = DescriptionDecider._score_candidate(product, content, brand_settings, tone)
            candidate = {
                "provider": "gemini",
                "provider_label": f"Google Gemini ({settings.GEMINI_MODEL})",
                "model": settings.GEMINI_MODEL,
                "source": source,
                "content": content,
                "scores": scores,
                "is_winner": True,
                "strengths": ["Directly selected Google Gemini engine", f"Overall Score: {scores['quality_score']}/100"]
            }
            decision_meta = {
                "winner_provider": "gemini",
                "winner_model": settings.GEMINI_MODEL,
                "winner_score": scores["quality_score"],
                "decision_rationale": f"Generated directly using Google Gemini ({settings.GEMINI_MODEL}) with a Quality Score of {scores['quality_score']}/100.",
                "score_comparison": {
                    "gemini_score": scores["quality_score"],
                    "winner": "gemini"
                },
                "mode": "gemini",
                "candidates": [candidate]
            }
            return content, source, decision_meta

        elif engine_mode_clean == "anthropic":
            content, source = AnthropicGenerator.generate(
                product, brand_settings, tone, language, word_count_preference
            )
            scores = DescriptionDecider._score_candidate(product, content, brand_settings, tone)
            candidate = {
                "provider": "anthropic",
                "provider_label": "Anthropic Claude 3.5 Sonnet",
                "model": settings.CLAUDE_MODEL,
                "source": source,
                "content": content,
                "scores": scores,
                "is_winner": True,
                "strengths": ["Directly selected Anthropic Claude engine", f"Overall Score: {scores['quality_score']}/100"]
            }
            decision_meta = {
                "winner_provider": "anthropic",
                "winner_model": settings.CLAUDE_MODEL,
                "winner_score": scores["quality_score"],
                "decision_rationale": f"Generated directly using Anthropic Claude ({settings.CLAUDE_MODEL}) with a Quality Score of {scores['quality_score']}/100.",
                "score_comparison": {
                    "anthropic_score": scores["quality_score"],
                    "winner": "anthropic"
                },
                "mode": "anthropic",
                "candidates": [candidate]
            }
            return content, source, decision_meta

        # DUAL MODE: Run Anthropic Claude and Google Gemini (Gemini 3.5 Lite) and decide the winner
        logger.info("Executing Dual-AI Decision Engine: Generating candidates with Anthropic Claude and Google Gemini...")

        content_claude, source_claude = AnthropicGenerator.generate(
            product, brand_settings, tone, language, word_count_preference
        )
        scores_claude = DescriptionDecider._score_candidate(product, content_claude, brand_settings, tone)

        content_gemini, source_gemini = GeminiGenerator.generate(
            product, brand_settings, tone, language, word_count_preference
        )
        scores_gemini = DescriptionDecider._score_candidate(product, content_gemini, brand_settings, tone)

        # Analyze strengths and differences
        strengths_claude = DescriptionDecider._identify_strengths(content_claude, scores_claude, product, brand_settings)
        strengths_gemini = DescriptionDecider._identify_strengths(content_gemini, scores_gemini, product, brand_settings)

        # Arbitrate and decide
        winner_provider, decision_rationale = DescriptionDecider._arbitrate_winner(
            scores_claude, scores_gemini,
            content_claude, content_gemini,
            product, brand_settings,
            provider_b_name=f"Google Gemini ({settings.GEMINI_MODEL})"
        )

        is_claude_winner = (winner_provider == "anthropic")
        winner_content = content_claude if is_claude_winner else content_gemini
        winner_source = source_claude if is_claude_winner else source_gemini
        winner_score = scores_claude["quality_score"] if is_claude_winner else scores_gemini["quality_score"]
        winner_model = settings.CLAUDE_MODEL if is_claude_winner else settings.GEMINI_MODEL

        candidate_claude_entry = {
            "provider": "anthropic",
            "provider_label": "Anthropic Claude 3.5 Sonnet",
            "model": settings.CLAUDE_MODEL,
            "source": source_claude,
            "content": content_claude,
            "scores": scores_claude,
            "is_winner": is_claude_winner,
            "strengths": strengths_claude
        }

        candidate_gemini_entry = {
            "provider": "gemini",
            "provider_label": f"Google Gemini ({settings.GEMINI_MODEL})",
            "model": settings.GEMINI_MODEL,
            "source": source_gemini,
            "content": content_gemini,
            "scores": scores_gemini,
            "is_winner": not is_claude_winner,
            "strengths": strengths_gemini
        }

        score_comparison = {
            "anthropic_score": scores_claude["quality_score"],
            "gemini_score": scores_gemini["quality_score"],
            "score_diff": round(abs(scores_claude["quality_score"] - scores_gemini["quality_score"]), 1),
            "winner": winner_provider,
            "seo_winner": "anthropic" if scores_claude["seo_score"] >= scores_gemini["seo_score"] else "gemini",
            "readability_winner": "anthropic" if scores_claude["readability_score"] >= scores_gemini["readability_score"] else "gemini",
            "tone_winner": "anthropic" if scores_claude["brand_tone_score"] >= scores_gemini["brand_tone_score"] else "gemini",
            "completeness_winner": "anthropic" if scores_claude["completeness_score"] >= scores_gemini["completeness_score"] else "gemini"
        }

        decision_meta = {
            "winner_provider": winner_provider,
            "winner_model": winner_model,
            "winner_score": winner_score,
            "decision_rationale": decision_rationale,
            "score_comparison": score_comparison,
            "mode": "dual",
            "candidates": [candidate_claude_entry, candidate_gemini_entry]
        }

        effective_source = f"{winner_source} (decided)" if winner_source in ["claude", "gemini"] else "dual_decided_mock"

        return winner_content, effective_source, decision_meta

    @staticmethod
    def _score_candidate(
        product: ProductCreate,
        content: Dict[str, Any],
        brand_settings: BrandSettingsBase,
        tone: str
    ) -> Dict[str, Any]:
        return QualityScorer.calculate_scores(
            product=product,
            title=content.get("title", ""),
            short_desc=content.get("short_description", ""),
            full_desc=content.get("full_description", ""),
            meta_title=content.get("meta_title", ""),
            meta_desc=content.get("meta_description", ""),
            brand_settings=brand_settings,
            tone=tone
        )

    @staticmethod
    def _identify_strengths(
        content: Dict[str, Any],
        scores: Dict[str, Any],
        product: ProductCreate,
        brand_settings: BrandSettingsBase
    ) -> List[str]:
        strengths = []
        if scores.get("seo_score", 0) >= 90:
            strengths.append(f"High SEO Rating ({scores['seo_score']}/100)")
        if scores.get("readability_score", 0) >= 85:
            strengths.append(f"Clear Readability ({scores['readability_score']}/100)")
        if scores.get("brand_tone_score", 0) >= 95:
            strengths.append("Strict Brand Voice Adherence")

        m_title = content.get("meta_title", "")
        if 30 <= len(m_title) <= 60:
            strengths.append(f"Optimal Meta Title ({len(m_title)} chars)")

        m_desc = content.get("meta_description", "")
        if 130 <= len(m_desc) <= 160:
            strengths.append(f"Ideal Meta Description Length ({len(m_desc)} chars)")

        primary_kws = product.primary_keywords or []
        if primary_kws and primary_kws[0].lower() in content.get("title", "").lower():
            strengths.append(f"Target Keyword in Title ('{primary_kws[0]}')")

        if not strengths:
            strengths.append(f"Comprehensive retail attributes ({scores.get('completeness_score', 0)}% completeness)")

        return strengths

    @staticmethod
    def _arbitrate_winner(
        scores_a: Dict[str, Any],
        scores_b: Dict[str, Any],
        content_a: Dict[str, Any],
        content_b: Dict[str, Any],
        product: ProductCreate,
        brand_settings: BrandSettingsBase,
        provider_b_name: str = "Google Gemini"
    ) -> Tuple[str, str]:
        score_a = scores_a.get("quality_score", 0)
        score_b = scores_b.get("quality_score", 0)

        seo_a = scores_a.get("seo_score", 0)
        seo_b = scores_b.get("seo_score", 0)

        read_a = scores_a.get("readability_score", 0)
        read_b = scores_b.get("readability_score", 0)

        tone_a = scores_a.get("brand_tone_score", 0)
        tone_b = scores_b.get("brand_tone_score", 0)

        diff = round(abs(score_a - score_b), 1)

        # Determine winner
        if score_a > score_b:
            winner = "anthropic"
            higher_score = score_a
            lower_score = score_b
            winner_name = "Anthropic Claude 3.5 Sonnet"
            alt_name = provider_b_name
        elif score_b > score_a:
            winner = "gemini"
            higher_score = score_b
            lower_score = score_a
            winner_name = provider_b_name
            alt_name = "Anthropic Claude 3.5 Sonnet"
        else:
            if seo_a >= seo_b:
                winner = "anthropic"
                winner_name = "Anthropic Claude 3.5 Sonnet"
                alt_name = provider_b_name
            else:
                winner = "gemini"
                winner_name = provider_b_name
                alt_name = "Anthropic Claude 3.5 Sonnet"
            higher_score = score_a
            lower_score = score_b

        # Formulate key reasoning points
        points = []
        if winner == "anthropic":
            if seo_a > seo_b:
                points.append(f"Higher SEO performance ({seo_a} vs {seo_b}) with tighter meta tag length calibration.")
            if read_a > read_b:
                points.append(f"Superior reading rhythm and sentence pacing ({read_a} vs {read_b}) tailored for retail.")
            if tone_a > tone_b:
                points.append(f"Better brand voice fidelity ({tone_a} vs {tone_b}) with strict prohibition compliance.")
            if not points:
                points.append(f"Achieved stronger overall copywriting balance (+{diff} pts higher quality score).")
        else:
            if seo_b > seo_a:
                points.append(f"Superior SEO keyword distribution and snippet readiness ({seo_b} vs {seo_a}).")
            if read_b > read_a:
                points.append(f"Enhanced conversion-driven clarity and sentence flow ({read_b} vs {read_a}).")
            if tone_b > tone_a:
                points.append(f"Closer adherence to selected brand tone parameters ({tone_b} vs {tone_a}).")
            if not points:
                points.append(f"Achieved higher overall copywriting score (+{diff} pts over alternative).")

        rationale = (
            f"Decided Winner: {winner_name} was selected as the Perfect Description with an Overall Quality Score of {higher_score}/100 "
            f"(+{diff} pts over {alt_name} at {lower_score}/100). "
            + " ".join(points)
        )

        return winner, rationale
