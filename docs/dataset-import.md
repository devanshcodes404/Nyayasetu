# Hugging Face Dataset Import Guide

NyayaSetu AI utilizes the primary public Indian case-law dataset:
**Hugging Face Dataset ID:** `Sumitedu/indian-case-laws`

## Important Architecture Rules
1. **Never Import via Serverless HTTP**: The complete dataset contains millions of records. Ingesting it via an ordinary Vercel Function will trigger timeouts (15s–60s limit).
2. **Explicit CLI Execution**: Ingestion, inspection, and text indexing must be executed locally or inside an asynchronous batch job worker.
3. **Idempotency**: Re-running imports does not create duplicate entries.

---

## 1. Inspecting the Dataset

Before running an import, discover configurations, splits, and actual field coverage:

```bash
cd backend
python scripts/inspect_huggingface_dataset.py
```

This script:
- Queries available dataset configurations and splits.
- Validates streaming capabilities.
- Inspects schema features and data types.
- Evaluates text coverage (indexable text vs. headnote text vs. metadata-only).
- Falls back to local verification fixtures if network access is offline.

---

## 2. Running Idempotent Batch Imports

### Dry-Run Mode
Test field mapping, validation, and rejection logic without writing to PostgreSQL:

```bash
python scripts/import_huggingface_cases.py --limit 100 --dry-run
```

### Batch Ingestion
Import a bounded sample (e.g. 100 records) into the database:

```bash
python scripts/import_huggingface_cases.py --limit 100 --batch-size 50
```

### CLI Arguments
- `--dataset-id`: Target dataset (default: `Sumitedu/indian-case-laws`)
- `--split`: Ingestion split (default: `train`)
- `--limit`: Maximum records to examine in this run
- `--batch-size`: Database commit transaction batch size
- `--dry-run`: Flag to simulate without committing
- `--no-resume`: Start from beginning rather than resuming from last processed external ID
- `--report-dir`: Directory for JSON execution summaries (default: `data/import-reports/`)

---

## 3. Text Indexing and Chunking

After records are imported into `judgments`, chunk the indexable text for keyword and semantic search:

```bash
python scripts/index_judgment_text.py --limit 100 --batch-size 25
```

