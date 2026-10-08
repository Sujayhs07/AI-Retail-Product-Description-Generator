from app.routers.health import router as health_router
from app.routers.products import router as products_router
from app.routers.generation import router as generation_router
from app.routers.batch import router as batch_router
from app.routers.analytics import router as analytics_router
from app.routers.settings import router as settings_router
from app.routers.export import router as export_router

__all__ = [
    "health_router",
    "products_router",
    "generation_router",
    "batch_router",
    "analytics_router",
    "settings_router",
    "export_router",
]
