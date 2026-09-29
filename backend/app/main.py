from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from app.core.config import settings
from app.core.database import init_db
from app.services.admin_seed_service import admin_seed_service
from app.api.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG,
)

# Enable CORS for React frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.v1.endpoints import admin

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix="/admin", tags=["Admin Dashboard Direct"])


@app.on_event("startup")
async def on_startup():
    """Ensure database tables exist and initial admin account is seeded on startup."""
    await init_db()
    await admin_seed_service.seed_initial_admin_if_empty()


@app.get("/health", tags=["Health"])
@app.get("/", tags=["Health"])
async def root_health_check():
    """Top-level health check and landing endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "version": "0.1.0",
        "docs_url": "/docs",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
