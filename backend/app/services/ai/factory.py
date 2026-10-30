"""
AI Provider Factory for dynamic selection between 'mock' and 'openai'.
"""
from app.core.config import settings
from app.services.ai.base import BaseAIProvider
from app.services.ai.mock_provider import MockAIProvider
from app.services.ai.openai_provider import OpenAIProvider


def get_ai_provider() -> BaseAIProvider:
    provider_name = (settings.AI_PROVIDER or "mock").lower()
    if provider_name == "openai" and settings.OPENAI_API_KEY:
        return OpenAIProvider()
    return MockAIProvider(dimension=settings.EMBEDDING_DIMENSION)

