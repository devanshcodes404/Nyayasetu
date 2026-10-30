"""
Vercel Python entrypoint for NyayaSetu AI Backend.
Exports the FastAPI app instance for Vercel Serverless Functions.
"""
from app.main import app

# Export for ASGI handler compatibility
__all__ = ["app"]

