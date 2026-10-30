"""
Text indexing script for court judgments.
Prepares token counts and document chunks for keyword and future semantic search.
Run via:
python scripts/index_judgment_text.py --limit 100
"""
import sys
import os
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.models.judgment import Judgment
from app.models.chunk import DocumentChunk
from app.services.documents.chunker import DocumentChunker
from app.core.config import settings


def index_judgments(limit: int = 100, batch_size: int = 25):
    print("=" * 60)
    print("NYAYASETU AI — JUDGMENT TEXT CHUNKER & INDEXER")
    print(f"Limit: {limit} | Batch size: {batch_size}")
    print("=" * 60)

    db = SessionLocal()
    chunker = DocumentChunker(chunk_size=500, chunk_overlap=80)
    indexed_count = 0

    try:
        judgments = (
            db.query(Judgment)
            .filter(Judgment.indexable_text.isnot(None))
            .limit(limit)
            .all()
        )
        print(f"Found {len(judgments)} judgments with indexable text to process.")

        for j in judgments:
            # Check if already chunked
            existing_chunks = db.query(DocumentChunk).filter(DocumentChunk.judgment_id == j.id).count()
            if existing_chunks > 0:
                continue

            chunks_data = chunker.chunk_text(j.indexable_text or "")
            chunk_objs = []
            for item in chunks_data:
                c = DocumentChunk(
                    judgment_id=j.id,
                    chunk_index=item["chunk_index"],
                    content=item["content"],
                    page_number=item["page_number"],
                    chunk_metadata=item["metadata"],
                )
                chunk_objs.append(c)

            if chunk_objs:
                db.add_all(chunk_objs)
                db.commit()
                indexed_count += 1
                print(f"Indexed judgment #{j.id}: '{j.title[:40]}...' into {len(chunk_objs)} chunks.")

        print(f"Indexing complete. Processed {indexed_count} judgments.")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Index judgment text")
    parser.add_argument("--limit", type=int, default=settings.HF_INDEXING_LIMIT)
    parser.add_argument("--batch-size", type=int, default=settings.HF_INDEXING_BATCH_SIZE)
    args = parser.parse_args()
    index_judgments(limit=args.limit, batch_size=args.batch_size)

