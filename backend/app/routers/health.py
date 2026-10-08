from fastapi import APIRouter
from app.config import settings

router = APIRouter(prefix="/api", tags=["Health"])

@router.get("/health")
def get_health():
    has_anthropic = bool(settings.ANTHROPIC_API_KEY.strip()) if settings.ANTHROPIC_API_KEY else False
    has_gemini = bool(settings.GEMINI_API_KEY.strip()) if settings.GEMINI_API_KEY else False

    if has_anthropic and has_gemini:
        ai_mode = "dual"
    elif has_anthropic:
        ai_mode = "claude"
    elif has_gemini:
        ai_mode = "gemini"
    else:
        ai_mode = "mock"

    return {
        "status": "online",
        "app_name": "CatalogCraft AI",
        "environment": settings.APP_ENV,
        "ai_mode": ai_mode,
        "claude_configured": has_anthropic,
        "anthropic_configured": has_anthropic,
        "gemini_configured": has_gemini,
        "claude_model": settings.CLAUDE_MODEL,
        "gemini_model": settings.GEMINI_MODEL,
        "version": "1.0.0"
    }
