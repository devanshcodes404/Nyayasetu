"""
FastAPI Main Application.
Configures CORS, middleware, API router, OpenAPI metadata, and graceful startup.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.logging import logger
from app.api.v1.router import api_router
from app.db.base import Base
from app.db.session import engine

# Automatically ensure tables exist on local SQLite if running dev without Alembic
if "sqlite" in (settings.DATABASE_URL or ""):
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered Court Case Management & Legal Research Platform for Indian Law",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS configuration
origins = settings.cors_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception at {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error", "detail": str(exc) if settings.DEBUG else None},
    )


# Attach API v1 Router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Welcome to NyayaSetu AI Backend API",
        "docs": "/api/docs",
        "health": "/api/v1/health",
        "version": "0.1.0",
    }

