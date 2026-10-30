"""
Document text parser for PDF, DOCX, and TXT files.
Extracts page-by-page text, detects empty or scanned documents, and preserves page numbers.
"""
from typing import Dict, Any, List, Optional
import io
import fitz  # PyMuPDF


class DocumentParser:
    @staticmethod
    def parse_txt(content: bytes) -> Dict[str, Any]:
        """Extracts text from raw UTF-8 / latin-1 TXT bytes."""
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            text = content.decode("latin-1", errors="replace")
        
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        return {
            "text": text,
            "page_count": 1,
            "pages": [{"page_number": 1, "text": text}],
            "paragraphs_count": len(paragraphs),
            "status": "FullText",
            "is_scanned": False,
        }

    @staticmethod
    def parse_pdf(content: bytes) -> Dict[str, Any]:
        """Extracts page-by-page text using PyMuPDF (fitz). Detects unreadable/scanned PDFs."""
        doc = fitz.open(stream=content, filetype="pdf")
        page_count = len(doc)
        pages = []
        total_text_length = 0

        for page_idx in range(page_count):
            page = doc.load_page(page_idx)
            page_text = page.get_text() or ""
            pages.append({
                "page_number": page_idx + 1,
                "text": page_text,
            })
            total_text_length += len(page_text.strip())

        doc.close()

        # Detection for scanned document requiring OCR
        avg_chars_per_page = total_text_length / max(page_count, 1)
        is_scanned = avg_chars_per_page < 30 and page_count > 0

        status = "ScannedImage" if is_scanned else ("FullText" if total_text_length > 0 else "Empty")
        full_text = "\n\n".join(p["text"] for p in pages if p["text"])

        return {
            "text": full_text,
            "page_count": page_count,
            "pages": pages,
            "status": status,
            "is_scanned": is_scanned,
        }

    @staticmethod
    def parse_docx(content: bytes) -> Dict[str, Any]:
        """Extracts text from DOCX files preserving paragraph structures."""
        try:
            import docx
            doc = docx.Document(io.BytesIO(content))
            paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            full_text = "\n\n".join(paragraphs)
            return {
                "text": full_text,
                "page_count": 1,
                "pages": [{"page_number": 1, "text": full_text}],
                "paragraphs_count": len(paragraphs),
                "status": "FullText" if full_text else "Empty",
                "is_scanned": False,
            }
        except Exception:
            # Fallback if docx structure is invalid
            return {
                "text": "",
                "page_count": 1,
                "pages": [],
                "status": "Failed",
                "is_scanned": False,
            }

    @classmethod
    def parse_bytes(cls, content: bytes, mime_type: str, filename: str) -> Dict[str, Any]:
        """Dispatches parser based on MIME type or file extension."""
        lower_name = filename.lower()
        if mime_type == "application/pdf" or lower_name.endswith(".pdf"):
            return cls.parse_pdf(content)
        elif mime_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"] or lower_name.endswith(".docx"):
            return cls.parse_docx(content)
        elif mime_type.startswith("text/") or lower_name.endswith(".txt"):
            return cls.parse_txt(content)
        else:
            return {
                "text": "",
                "page_count": 0,
                "pages": [],
                "status": "UnsupportedType",
                "is_scanned": False,
            }

