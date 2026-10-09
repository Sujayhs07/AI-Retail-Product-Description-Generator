import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.seed.seed_data import seed_database

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database(db)
    db.close()

def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "online"
        assert "ai_mode" in data

def test_products_list_endpoint():
    with TestClient(app) as client:
        response = client.get("/api/products")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data

def test_brand_settings_endpoint():
    with TestClient(app) as client:
        response = client.get("/api/settings/brand")
        assert response.status_code == 200
        data = response.json()
        assert "brand_name" in data

def test_generate_description_mock():
    with TestClient(app) as client:
        payload = {
            "product": {
                "name": "Test Wireless Mouse",
                "category": "Electronics",
                "brand": "TechBrand",
                "price": 29.99,
                "features": ["Ergonomic", "Bluetooth 5.0"],
                "primary_keywords": ["wireless mouse"]
            },
            "tone": "Professional",
            "language": "English",
            "word_count_preference": "Medium",
            "save_to_catalog": True
        }
        response = client.post("/api/generate-description", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "generated_content" in data
        assert data["generated_content"]["title"] != ""

def test_security_headers():
    with TestClient(app) as client:
        response = client.get("/api/health")
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert "1; mode=block" in response.headers.get("X-XSS-Protection", "")

def test_csv_export_formula_sanitization():
    from app.services.export.exporter import ContentExporter
    malicious_item = {
        "title": "=cmd|' /C calc'!A0",
        "description": "@SUM(1+1)",
        "bullets": "+12345",
        "category": "-dangerous"
    }
    csv_str = ContentExporter.to_csv_string([malicious_item])
    # Ensure dangerous prefixes are escaped with apostrophe
    assert "'=cmd|" in csv_str
    assert "'@SUM" in csv_str
    assert "'+12345" in csv_str
    assert "'-dangerous" in csv_str
