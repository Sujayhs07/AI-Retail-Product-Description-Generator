from app.schemas.product import ProductCreate
from app.schemas.brand_settings import BrandSettingsBase
from app.services.ai.mock_generator import MockGenerator

def test_mock_generator_output():
    product = ProductCreate(
        sku="TEST-100",
        name="Wireless Noise Cancelling Earbuds",
        brand="TechSound",
        category="Electronics",
        price=99.99,
        features=["ANC", "Bluetooth 5.3", "Water Resistant"],
        specifications={"Battery": "24h"},
        target_audience="Music lovers",
        primary_keywords=["wireless earbuds"],
        material="Plastic",
        color="Black"
    )
    brand_settings = BrandSettingsBase()

    result = MockGenerator.generate(product, brand_settings, tone="Professional", language="English", word_count_preference="Medium")

    assert "TechSound" in result["title"]
    assert len(result["short_description"]) > 10
    assert len(result["full_description"]) > 20
    assert isinstance(result["highlights"], list)
    assert len(result["meta_title"]) > 0
    assert len(result["meta_description"]) > 0
    assert isinstance(result["warnings"], list)
