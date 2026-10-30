"""
Inspection script for Hugging Face corpus 'Sumitedu/indian-case-laws'.
Discovers configurations, splits, features, streaming support, and text coverage.
Run via:
python scripts/inspect_huggingface_dataset.py
"""
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings


def inspect_dataset():
    dataset_id = settings.HF_DATASET_ID
    print("=" * 60)
    print(f"NYAYASETU AI — HUGGING FACE DATASET INSPECTOR")
    print(f"Dataset Target: {dataset_id}")
    print("=" * 60)

    try:
        from datasets import get_dataset_config_names, get_dataset_split_names, load_dataset
        print("[1/5] Querying dataset configurations...")
        try:
            configs = get_dataset_config_names(dataset_id)
            print(f"Available Configurations: {configs}")
            chosen_config = configs[0] if configs else None
        except Exception as e:
            print(f"Could not fetch configs dynamically ({e}). Defaulting to 'default'.")
            chosen_config = None

        print(f"[2/5] Querying splits for config '{chosen_config}'...")
        try:
            splits = get_dataset_split_names(dataset_id, chosen_config)
            print(f"Available Splits: {splits}")
            chosen_split = splits[0] if splits else "train"
        except Exception as e:
            print(f"Could not fetch splits dynamically ({e}). Defaulting to 'train'.")
            chosen_split = "train"

        print(f"[3/5] Testing streaming connection for split '{chosen_split}'...")
        ds_stream = load_dataset(dataset_id, name=chosen_config, split=chosen_split, streaming=True)
        print("Streaming successfully initialized.")

        print("[4/5] Reading representative sample record...")
        sample_record = next(iter(ds_stream))
        print("Sample Schema Keys Discovered:")
        for k in sorted(sample_record.keys()):
            val_type = type(sample_record[k]).__name__
            has_val = bool(sample_record[k])
            print(f"  - {k} ({val_type}) [populated: {has_val}]")

        print("[5/5] Text coverage evaluation:")
        idx_text = sample_record.get("indexable_text") or sample_record.get("text") or ""
        headnote = sample_record.get("headnote_text") or sample_record.get("headnote") or ""
        print(f"  Indexable Text length: {len(idx_text)} characters")
        print(f"  Headnote Text length:  {len(headnote)} characters")
        print("Dataset inspection completed successfully.")

    except Exception as exc:
        print("\n" + "!" * 60)
        print("NOTICE: Hugging Face online hub could not be reached or required package not loaded.")
        print(f"Exception Type: {type(exc).__name__}")
        print(f"Details: {exc}")
        print("!" * 60)
        print("\nEvaluating documented schema & local verification fixture...")
        demo_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "demo", "sample_judgments.json")
        )
        if os.path.exists(demo_path):
            with open(demo_path, "r", encoding="utf-8") as f:
                samples = json.load(f)
            print(f"Loaded {len(samples)} representative local corpus samples.")
            first = samples[0]
            print(f"Verified Candidate Keys ({len(first.keys())} fields):")
            for k in sorted(first.keys()):
                print(f"  - {k}: {type(first[k]).__name__}")
            print(f"Text Availability in sample: {first.get('text_availability_status', 'FullText')}")
            print("Local dataset schema verification succeeded.")
        else:
            print("No local fixture found. Ensure data/demo/sample_judgments.json exists.")


if __name__ == "__main__":
    inspect_dataset()

