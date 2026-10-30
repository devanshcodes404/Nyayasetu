"""
Mock AI Provider for development, testing, and offline environments.
Clearly labels outputs as simulated mock responses.
"""
from typing import List, Dict, Any, Optional
from app.services.ai.base import BaseAIProvider


class MockAIProvider(BaseAIProvider):
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension

    def generate_completion(self, prompt: str, system_message: Optional[str] = None) -> str:
        return (
            "[MOCK AI RESPONSE - PART 2 DEMO] This is a mock response from NyayaSetu AI. "
            "Real LLM responses are scheduled for PART 2. Prompt received: " + prompt[:100]
        )

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        # Returns deterministic normalized mock vectors
        results = []
        for text in texts:
            val = (len(text) % 100) / 100.0
            vector = [val] * self.dimension
            results.append(vector)
        return results

    def summarize_judgment(self, judgment_text: str, headnote: Optional[str] = None) -> Dict[str, Any]:
        return {
            "summary_type": "mock_development_summary",
            "key_legal_issues": ["Interpretation of statutory provisions (Mock)", "Procedural compliance (Mock)"],
            "held_disposition": "Court disposition based on preliminary findings (Mock)",
            "notable_citations": ["AIR 1973 SC 1461 (Mock Reference)"],
            "disclaimer": "This is a mock development summary. Real LLM summarization is reserved for PART 2.",
        }

