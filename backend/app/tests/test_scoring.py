from app.schemas.product import ProductCreate
from app.schemas.brand_settings import BrandSettingsBase
from app.services.scoring.quality_scorer import QualityScorer

def test_quality_scorer():
    product = ProductCreate(
        sku="TEST-200",
        name="Organic Leather Tote",
        brand="Luxe",
        category="Fashion",
        price=150.0,
        features=["Genuine Leather", "Laptop Compartment"],
        specifications={"Capacity": "15L"},
        target_audience="Working women",
        primary_keywords=["leather tote"],
        material="Leather"
    )
    brand_settings = BrandSettingsBase(prohibited_words=["cheap", "junk"])

    scores = QualityScorer.calculate_scores(
        product=product,
        title="Luxe Organic Leather Tote",
        short_desc="Stylish leather tote for work.",
        full_desc="The Luxe Organic Leather Tote is engineered for working women with genuine leather.",
        meta_title="Buy Luxe Leather Tote Bag Online",
        meta_desc="Discover the Luxe Organic Leather Tote for daily work essentials.",
        brand_settings=brand_settings,
        tone="Professional"
    )

    assert 0 <= scores["quality_score"] <= 100
    assert 0 <= scores["completeness_score"] <= 100
    assert 0 <= scores["seo_score"] <= 100
    assert 0 <= scores["readability_score"] <= 100
    assert 0 <= scores["brand_tone_score"] <= 100
