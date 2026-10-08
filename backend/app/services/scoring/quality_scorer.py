import re
from typing import Dict, Any, List, Tuple
from app.schemas.product import ProductCreate
from app.schemas.brand_settings import BrandSettingsBase

class QualityScorer:
    @staticmethod
    def calculate_scores(
        product: ProductCreate,
        title: str,
        short_desc: str,
        full_desc: str,
        meta_title: str,
        meta_desc: str,
        brand_settings: BrandSettingsBase,
        tone: str = "Professional"
    ) -> Dict[str, Any]:
        """
        Calculates 0-100 quality scores across Completeness, SEO, Readability, and Brand Tone.
        """
        # 1. Completeness Score
        completeness_score, missing_fields = QualityScorer._calc_completeness(product)
        
        # 2. SEO Score
        seo_score, seo_recommendations = QualityScorer._calc_seo(
            product, title, full_desc, meta_title, meta_desc
        )
        
        # 3. Readability Score
        readability_score, readability_recommendations = QualityScorer._calc_readability(full_desc)
        
        # 4. Brand Tone Score
        brand_score, brand_warnings = QualityScorer._calc_brand_tone(
            title, short_desc, full_desc, brand_settings, tone
        )
        
        # Overall Score calculation
        overall_score = round(
            (0.30 * completeness_score) +
            (0.30 * seo_score) +
            (0.20 * readability_score) +
            (0.20 * brand_score),
            1
        )
        
        # Consolidate actionable recommendations & warnings
        recommendations = []
        if missing_fields:
            recommendations.append(f"Add missing product details for richer content: {', '.join(missing_fields[:3])}.")
        recommendations.extend(seo_recommendations)
        recommendations.extend(readability_recommendations)
        recommendations.extend(brand_warnings)

        return {
            "completeness_score": completeness_score,
            "seo_score": seo_score,
            "readability_score": readability_score,
            "brand_tone_score": brand_score,
            "quality_score": overall_score,
            "recommendations": recommendations
        }

    @staticmethod
    def _calc_completeness(product: ProductCreate) -> Tuple[float, List[str]]:
        fields_to_check = {
            "Product Name": bool(product.name),
            "Brand": bool(product.brand),
            "Category": bool(product.category),
            "Price": product.price is not None and product.price > 0,
            "Features": bool(product.features and len(product.features) > 0),
            "Specifications": bool(product.specifications and len(product.specifications) > 0),
            "Target Audience": bool(product.target_audience),
            "Primary Keywords": bool(product.primary_keywords and len(product.primary_keywords) > 0),
            "USP": bool(product.usp),
            "Image URL": bool(product.image_url),
        }
        
        present_count = sum(1 for v in fields_to_check.values() if v)
        missing_fields = [k for k, v in fields_to_check.items() if not v]
        
        score = round((present_count / len(fields_to_check)) * 100, 1)
        return score, missing_fields

    @staticmethod
    def _calc_seo(
        product: ProductCreate,
        title: str,
        full_desc: str,
        meta_title: str,
        meta_desc: str
    ) -> Tuple[float, List[str]]:
        score = 100.0
        recs = []

        primary_kw = (product.primary_keywords or [])
        full_text = f"{title} {full_desc}".lower()

        # Check primary keyword presence
        if primary_kw:
            found_kws = [kw for kw in primary_kw if kw.lower() in full_text]
            if not found_kws:
                score -= 25.0
                recs.append(f"Primary keyword '{primary_kw[0]}' is missing from product title or description.")
            else:
                # Check keyword stuffing (density > 5%)
                first_kw = primary_kw[0].lower()
                count = full_text.count(first_kw)
                word_count = len(full_text.split())
                if word_count > 0 and (count / word_count) > 0.05:
                    score -= 15.0
                    recs.append(f"Keyword '{primary_kw[0]}' appears too frequently; lower density for natural SEO.")
        else:
            score -= 15.0
            recs.append("No primary keywords were provided for SEO optimization.")

        # Meta title length (optimal 30-60 chars)
        m_title_len = len(meta_title or "")
        if m_title_len < 20 or m_title_len > 70:
            score -= 10.0
            recs.append(f"Meta title length is {m_title_len} chars; optimal length is 30–60 characters.")

        # Meta description length (optimal 120-160 chars)
        m_desc_len = len(meta_desc or "")
        if m_desc_len < 100 or m_desc_len > 170:
            score -= 10.0
            recs.append(f"Meta description length is {m_desc_len} chars; aim for approximately 140–160 characters.")

        return max(0.0, round(score, 1)), recs

    @staticmethod
    def _calc_readability(full_desc: str) -> Tuple[float, List[str]]:
        words = full_desc.split()
        if not words:
            return 0.0, ["Description is empty."]

        score = 90.0
        recs = []

        sentences = [s for s in re.split(r'[.!?]+', full_desc) if s.strip()]
        if sentences:
            avg_sentence_len = len(words) / len(sentences)
            if avg_sentence_len > 25:
                score -= 15.0
                recs.append("Sentences are quite long; consider shortening for clearer mobile reading.")
            elif avg_sentence_len < 6:
                score -= 10.0
                recs.append("Sentences are overly brief or choppy.")

        avg_word_len = sum(len(w) for w in words) / len(words)
        if avg_word_len > 6.5:
            score -= 10.0
            recs.append("High vocabulary complexity; simplify terms for general retail shoppers.")

        return max(0.0, round(score, 1)), recs

    @staticmethod
    def _calc_brand_tone(
        title: str,
        short_desc: str,
        full_desc: str,
        brand_settings: BrandSettingsBase,
        tone: str
    ) -> Tuple[float, List[str]]:
        score = 100.0
        warnings = []
        combined_text = f"{title} {short_desc} {full_desc}".lower()

        # Check prohibited words
        prohibited = brand_settings.prohibited_words or []
        for word in prohibited:
            if word.lower() in combined_text:
                score -= 20.0
                warnings.append(f"Contains prohibited brand phrase: '{word}'.")

        # Check preferred words bonus/penalty
        preferred = brand_settings.preferred_words or []
        if preferred:
            matched_pref = [w for w in preferred if w.lower() in combined_text]
            if not matched_pref:
                score -= 10.0

        return max(0.0, round(score, 1)), warnings
