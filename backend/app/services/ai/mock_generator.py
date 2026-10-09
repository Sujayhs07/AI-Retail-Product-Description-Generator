from typing import Dict, Any, List
from app.schemas.product import ProductCreate
from app.schemas.brand_settings import BrandSettingsBase

class MockGenerator:
    @staticmethod
    def generate(
        product: ProductCreate,
        brand_settings: BrandSettingsBase = None,
        tone: str = "Professional",
        language: str = "English",
        word_count_preference: str = "Medium",
        provider: str = "claude"
    ) -> Dict[str, Any]:
        """
        Generates realistic, tailored product copy without external AI API.
        Supports distinct stylistic flavors for Anthropic Claude and Google Gemini.
        """
        if brand_settings is None:
            brand_settings = BrandSettingsBase()

        p_name = product.name
        p_brand = product.brand or brand_settings.brand_name or "Premium Retail"
        p_cat = product.category
        
        features = product.features or []
        specs = product.specifications or {}
        audience = product.target_audience or "shoppers looking for quality and reliability"
        usp = product.usp or f"crafted with precision for modern {p_cat.lower()} needs"
        primary_kws = product.primary_keywords or [p_name]
        sec_kws = product.secondary_keywords or []
        kw_lead = primary_kws[0] if primary_kws else p_name

        is_gemini = (provider.lower() in ["gemini", "google"])

        if is_gemini:
            # Google Gemini style: Highly structured, ultra-fast, high-converting feature clarity
            tone_intros = {
                "Professional": f"Engineered for high-impact performance, the {p_name} by {p_brand} delivers smart utility and uncompromising dependability for {audience}.",
                "Premium / Luxury": f"Refined craftsmanship meets modern innovation with the {p_name} by {p_brand}. Designed exclusively for {audience} who value distinction.",
                "Friendly": f"Meet the all-new {p_name} from {p_brand}—your smart daily companion designed to make life easier and more enjoyable.",
                "Minimal": f"Essential clarity. The {p_name} by {p_brand} pairs understated elegance with purposeful functionality.",
                "Technical": f"Precision-engineered with cutting-edge standards, the {p_name} from {p_brand} delivers measurable output and robust durability.",
                "Playful": f"Bring excitement to your day with the innovative {p_name} by {p_brand}! Built to inspire and delight.",
                "Eco-conscious": f"Sustainably crafted for eco-minded shoppers, the {p_name} by {p_brand} delivers premium performance with mindful environmental responsibility."
            }
            intro = tone_intros.get(tone, tone_intros["Professional"])

            feature_bullets = ""
            if features:
                feature_bullets = f" Core benefits include {', '.join(features[:3])}."

            spec_details = ""
            if product.material:
                spec_details += f" Constructed from {product.material}."
            if product.dimensions:
                spec_details += f" Precise dimensions: {product.dimensions}."
            if product.color:
                spec_details += f" Modern {product.color} aesthetic."
            if product.weight:
                spec_details += f" Ergonomic weight of {product.weight}."

            usp_sentence = f" {usp.capitalize()}." if usp else ""

            if word_count_preference == "Short":
                full_desc = f"{intro}{feature_bullets}{usp_sentence}".strip()
            elif word_count_preference == "Long":
                full_desc = (
                    f"{intro}{feature_bullets}{spec_details}{usp_sentence} "
                    f"Tailored specifically for {audience}, this solution maximizes value across all your {p_cat.lower()} requirements. "
                    f"Experience seamless quality with the {p_name} today."
                ).strip()
            else:
                full_desc = f"{intro}{feature_bullets}{spec_details}{usp_sentence} Perfect for {audience}.".strip()

            brand_title = p_name if p_name.lower().startswith(p_brand.lower()) else f"{p_brand} {p_name}"
            title = f"{brand_title} - Smart {p_cat} with {kw_lead}"
            short_desc = f"{intro} Highlights {', '.join(features[:2]) if features else 'versatile specs'} for {audience}."

            highlights = []
            if features:
                highlights.extend([f"Key Advantage: {f}" for f in features[:4]])
            if product.material:
                highlights.append(f"Material: {product.material}")
            if not highlights:
                highlights = [f"Certified {p_brand} engineering", f"Designed for {p_cat}", "Reliable performance"]

            meta_title = f"{p_name} | Buy {p_brand} {kw_lead}"[:56]
            meta_desc = f"Shop the {p_name} by {p_brand}. Features {kw_lead} for {audience}. High performance and fast shipping."[:148]

        else:
            # Anthropic Claude style: Rich storytelling, sensory detail, nuanced brand tone
            tone_intros = {
                "Professional": f"Engineered for exceptional performance, the {p_name} by {p_brand} delivers uncompromised quality for {audience}.",
                "Premium / Luxury": f"Indulge in sophistication with the {p_name} by {p_brand}. Designed for discerning individuals who appreciate elegance and luxury.",
                "Friendly": f"Meet your new favorite item! The {p_name} from {p_brand} brings convenience, style, and everyday enjoyment.",
                "Minimal": f"{p_name} by {p_brand}. Clean design, essential functionality, designed for modern simplicity.",
                "Technical": f"The {p_name} is a high-specification solution from {p_brand}, optimized for precise operational efficiency.",
                "Playful": f"Upgrade your day with the exciting {p_name}! Brought to you by {p_brand}, it's ready to elevate your routine with fun and utility.",
                "Eco-conscious": f"Thoughtfully designed with sustainability in mind, the {p_name} by {p_brand} offers reliable performance with lower environmental impact."
            }
            intro = tone_intros.get(tone, tone_intros["Professional"])

            feature_text = ""
            if features:
                f_list = ", ".join(features[:3])
                feature_text = f" Key highlights include {f_list}."

            spec_text = ""
            if product.material:
                spec_text += f" Constructed from high-grade {product.material}."
            if product.color:
                spec_text += f" Available in a stylish {product.color} finish."
            if product.dimensions:
                spec_text += f" Dimensions measure {product.dimensions}."
            if product.weight:
                spec_text += f" Lightweight build weighing {product.weight}."

            usp_sentence = f" {usp.capitalize()}." if usp else ""

            if word_count_preference == "Short":
                full_desc = f"{intro}{feature_text}{usp_sentence}".strip()
            elif word_count_preference == "Long":
                full_desc = (
                    f"{intro}{feature_text}{spec_text}{usp_sentence} "
                    f"Tailored specifically for {audience}, this product seamlessly integrates into your daily workflow. "
                    f"Whether for home or commercial use, the {p_name} stands as an outstanding addition to your {p_cat.lower()} setup."
                ).strip()
            else:
                full_desc = f"{intro}{feature_text}{spec_text}{usp_sentence} Perfectly suited for {audience}.".strip()

            title = p_name if p_name.lower().startswith(p_brand.lower()) else f"{p_brand} {p_name}"
            if product.color and product.color.lower() not in title.lower():
                title += f" ({product.color})"

            short_desc = f"{intro} Featuring {', '.join(features[:2]) if features else 'essential features'} for {audience}."

            highlights = []
            if features:
                highlights.extend(features[:4])
            if product.material:
                highlights.append(f"Material: {product.material}")
            if product.dimensions:
                highlights.append(f"Dimensions: {product.dimensions}")
            if not highlights:
                highlights = [f"Authentic {p_brand} quality", f"Ideal for {p_cat} applications", "Designed for long-lasting performance"]

            meta_title = f"Buy {p_brand} {kw_lead} | Official {p_cat} Store"[:58]
            meta_desc = f"Discover the {p_name} by {p_brand}. {short_desc}"[:155]

        # Append mandatory disclaimer if present
        if brand_settings.mandatory_disclaimer:
            full_desc += f" Note: {brand_settings.mandatory_disclaimer}"

        # Suggested keywords
        suggested_kws = list(set([kw.strip() for kw in (primary_kws + sec_kws + [p_cat, p_brand, product.material or ""]) if kw]))

        # Warnings logic
        warnings = []
        if not product.material:
            warnings.append("Material is unspecified in product details.")
        if not product.dimensions:
            warnings.append("Dimensions are missing; consider specifying for complete product details.")
        if not product.target_audience:
            warnings.append("Target audience was not provided.")
        if not product.primary_keywords:
            warnings.append("No primary SEO keywords were supplied.")
        if not product.price:
            warnings.append("Pricing information is absent.")

        return {
            "title": title,
            "short_description": short_desc,
            "full_description": full_desc,
            "highlights": highlights,
            "meta_title": meta_title,
            "meta_description": meta_desc,
            "suggested_keywords": suggested_kws[:6],
            "warnings": warnings
        }
