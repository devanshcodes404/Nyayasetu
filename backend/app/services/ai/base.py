"""
Abstract base class for AI providers (Part 2 interface).
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseAIProvider(ABC):
    @abstractmethod
    def generate_completion(self, prompt: str, system_message: Optional[str] = None) -> str:
        """Generates text completion."""
        pass

    @abstractmethod
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generates numerical vector embeddings for the provided texts."""
        pass

    @abstractmethod
    def summarize_judgment(self, judgment_text: str, headnote: Optional[str] = None) -> Dict[str, Any]:
        """Produces structured summary of a court judgment."""
        pass

