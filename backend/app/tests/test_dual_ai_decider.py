import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal, init_db
from app.seed.seed_data import seed_database
from app.schemas.product import ProductCreate
from app.schemas.brand_settings import BrandSettingsBase
from app.services.ai.description_decider import DescriptionDecider

@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    db = SessionLocal()
    seed_database(db)
    db.close()

def test_dual_ai_decider_flow():
    prod = ProductCreate(
        name="Ultra ANC Headphones",
        category="Electronics",
        brand="AuraSound",
        price=199.99,
        features=["Active Noise Cancellation", "40-Hour Battery"],
        primary_keywords=["noise cancelling headphones"]
    )
    brand_settings = BrandSettingsBase(
        brand_name="AuraSound",
        brand_voice="Premium and technical",
        preferred_words=["precision"],
        prohibited_words=["cheap"]
    )

    winner_content, source, decision_meta = DescriptionDecider.decide_perfect_description(
        product=prod,
        brand_settings=brand_settings,
        tone="Professional",
        language="English",
        word_count_preference="Medium",
        engine_mode="dual"
    )

    assert "title" in winner_content
    assert "short_description" in winner_content
    assert "full_description" in winner_content
    assert "candidates" in decision_meta
    assert len(decision_meta["candidates"]) == 2
    assert decision_meta["winner_provider"] in ["anthropic", "gemini"]
    assert "decision_rationale" in decision_meta
    assert decision_meta["winner_score"] > 0

def test_api_generate_with_engine_modes():
    with TestClient(app) as client:
        payload = {
            "product": {
                "name": "Smart Fitness Band",
                "category": "Sports and Fitness",
                "brand": "FitCore",
                "price": 49.99,
                "features": ["Heart Rate Monitor", "Step Counter", "Water Resistant"],
                "primary_keywords": ["fitness tracker"]
            },
            "tone": "Professional",
            "language": "English",
            "word_count_preference": "Medium",
            "save_to_catalog": True,
            "engine": "dual"
        }

        # 1. Dual mode (Anthropic Claude vs Google Gemini)
        res_dual = client.post("/api/generate-description", json=payload)
        assert res_dual.status_code == 200
        data_dual = res_dual.json()["generated_content"]
        assert "candidates_data" in data_dual
        assert len(data_dual["candidates_data"]) == 2
        assert "decision_rationale" in data_dual
        assert data_dual["decision_rationale"] != ""

        # 2. Gemini engine explicitly
        payload["engine"] = "gemini"
        res_gemini = client.post("/api/generate-description", json=payload)
        assert res_gemini.status_code == 200
        data_gemini = res_gemini.json()["generated_content"]
        assert "title" in data_gemini

        # 3. Anthropic engine explicitly
        payload["engine"] = "anthropic"
        res_ant = client.post("/api/generate-description", json=payload)
        assert res_ant.status_code == 200
        data_ant = res_ant.json()["generated_content"]
        assert "title" in data_ant

def test_api_key_empty_fallback_notice():
    """Verify that when API keys are empty, api_key_notice is returned with is_missing: True and fallback to mock."""
    prod = ProductCreate(
        name="Offline Test Item",
        category="Electronics",
        brand="TestBrand",
        price=29.99,
        features=["Long Battery Life"],
        primary_keywords=["battery"]
    )
    brand_settings = BrandSettingsBase(
        brand_name="TestBrand",
        brand_voice="Friendly",
        preferred_words=[],
        prohibited_words=[]
    )

    _, _, meta = DescriptionDecider.decide_perfect_description(
        product=prod,
        brand_settings=brand_settings,
        engine_mode="dual"
    )

    assert "api_key_notice" in meta
    # If keys are empty or test env has no real keys:
    notice = meta["api_key_notice"]
    assert "is_missing" in notice

    with TestClient(app) as client:
        res = client.post("/api/generate-description", json={
            "product": {
                "name": "Offline Headset",
                "category": "Electronics",
                "brand": "Aura",
                "price": 59.99,
                "features": ["Wireless"],
                "primary_keywords": ["headset"]
            },
            "tone": "Professional",
            "language": "English",
            "word_count_preference": "Medium",
            "save_to_catalog": True,
            "engine": "dual"
        })
        assert res.status_code == 200
        gen = res.json()["generated_content"]
        assert "api_key_notice" in gen

