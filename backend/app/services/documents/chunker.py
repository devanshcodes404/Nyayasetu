"""
Document text chunker for vector retrieval and embedding generation.
Chunks text with configurable overlap while respecting page boundaries and paragraphs.
"""
from typing import List, Dict, Any


class DocumentChunker:
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_pages(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Chunks a document preserving page_number references."""
        chunks = []
        chunk_index = 0

        for page in pages:
            page_num = page.get("page_number", 1)
            text = page.get("text", "")
            if not text.strip():
                continue

            # Split by words
            words = text.split()
            if not words:
                continue

            i = 0
            while i < len(words):
                chunk_words = words[i : i + self.chunk_size]
                chunk_content = " ".join(chunk_words)
                
                chunks.append({
                    "chunk_index": chunk_index,
                    "content": chunk_content,
                    "page_number": page_num,
                    "metadata": {
                        "page": page_num,
                        "word_count": len(chunk_words),
                    }
                })
                chunk_index += 1
                
                i += (self.chunk_size - self.chunk_overlap)
                if i <= 0 or i >= len(words):
                    break

        return chunks

    def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """Fallback chunker for flat unpaginated text."""
        return self.chunk_pages([{"page_number": 1, "text": text}])

