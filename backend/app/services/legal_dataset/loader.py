"""
Hugging Face dataset loader supporting streaming, offline demo fixtures, and safe iteration.
"""
from typing import Iterator, Dict, Any, Optional
import os
import json
from app.core.config import settings
from app.core.logging import logger


class DatasetLoader:
    def __init__(
        self,
        dataset_id: str = settings.HF_DATASET_ID,
        config: Optional[str] = settings.HF_DATASET_CONFIG,
        split: str = settings.HF_DATASET_SPLIT,
        streaming: bool = settings.HF_DATASET_STREAMING,
    ):
        self.dataset_id = dataset_id
        self.config = config
        self.split = split
        self.streaming = streaming

    def load_stream(self) -> Iterator[Dict[str, Any]]:
        """
        Attempts to stream records from Hugging Face dataset.
        If network is offline or inaccessible, gracefully falls back to local demo fixtures.
        """
        # If offline or streaming is disabled in test, load local fixture immediately
        if not self.streaming:
            demo_fixture_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "data", "demo", "sample_judgments.json")
            )
            if os.path.exists(demo_fixture_path):
                with open(demo_fixture_path, "r", encoding="utf-8") as f:
                    for record in json.load(f):
                        yield record
            return

        try:
            from datasets import load_dataset
            logger.info(f"Connecting to Hugging Face dataset {self.dataset_id} (split={self.split}, streaming={self.streaming})")
            ds = load_dataset(
                self.dataset_id,
                name=self.config,
                split=self.split,
                streaming=True,
            )
            for record in ds:
                yield record
            return
        except Exception as exc:
            logger.warning(f"Could not stream directly from Hugging Face ({type(exc).__name__}: {exc}). Checking local demo fixtures...")

        # Fallback to local demo dataset fixture if present
        demo_fixture_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "data", "demo", "sample_judgments.json")
        )
        if os.path.exists(demo_fixture_path):
            logger.info(f"Loading local sample judgments from fixture: {demo_fixture_path}")
            with open(demo_fixture_path, "r", encoding="utf-8") as f:
                records = json.load(f)
                for record in records:
                    yield record
        else:
            logger.warning("No local demo fixture found at data/demo/sample_judgments.json.")
