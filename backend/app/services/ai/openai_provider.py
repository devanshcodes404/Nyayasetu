"""
OpenAI Provider implementation (Part 2 interface).
Does not initialize external network calls during application startup.
"""
from typing import List, Dict, Any, Optional
from app.services.ai.base import BaseAIProvider
from app.core.config import settings
from app.core.logging import logger


class OpenAIProvider(BaseAIProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.OPENAI_MODEL
        self.embedding_model = settings.OPENAI_EMBEDDING_MODEL

    def _ensure_client(self):
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not configured in environment settings.")

    def generate_completion(self, prompt: str, system_message: Optional[str] = None) -> str:
        self._ensure_client()
        # In PART 2, invokes openai.OpenAI client
        return f"[OpenAI Provider Ready] Prompt queued for {self.model}: {prompt[:50]}..."

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        self._ensure_client()
        # In PART 2, invokes embeddings.create
        return [[0.0] * settings.EMBEDDING_DIMENSION for _ in texts]

    def summarize_judgment(self, judgment_text: str, headnote: Optional[str] = None) -> Dict[str, Any]:
        self._ensure_client()
        return {
            "summary_type": "openai_llm",
            "message": "Configured for Part 2 completion",
        }

