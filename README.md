# NyayaSetu AI — Court Case Management & Legal Research Platform
## PART 1: Full-Stack Foundation, Real Indian Case-Law Dataset & Vercel Deployment

NyayaSetu AI is an AI-powered legal technology SaaS platform engineered for advocates, law chambers, and legal researchers in India.

This repository contains the complete full-stack implementation of **PART 1**, establishing the application foundation, multi-tenant case management, document parsing vault, real Indian case-law dataset ingestion pipeline, database-backed judgment search, and readiness interfaces for PART 2 AI features.

---

## 1. Key Features in PART 1

1. **Court Case Brief Management**:
   - Create, list, edit, and track active court briefs across Indian courts and tribunals.
   - Track docket numbers, filing dates, opposing parties, and upcoming hearing schedules.
   - Resource-level multi-tenant security (`owner_id` enforcement).
2. **Indian Case-Law Ingestion Pipeline**:
   - Integrated with the primary public Indian judgment dataset: `Sumitedu/indian-case-laws`.
   - Streaming, batching, idempotency, duplicate detection, and schema normalization.
   - CLI scripts for inspection, dry-runs, and batch loading.
3. **Database-Backed Judgment Search**:
   - Parameterized search across case titles, petitioners, respondents, citations (Neutral & Law Reports), CNR numbers, courts, and decision years.
   - Full pagination, text availability status classification (`FullText`, `HeadnoteOnly`, `MetadataOnly`), and source links.
4. **Document Ingestion Vault**:
   - Secure upload and parsing of PDF (PyMuPDF), DOCX (python-docx), and TXT brief files.
   - SHA-256 checksum verification, scanned document detection, and page counting.
   - Storage adapter supporting Vercel Blob private storage and local disk development fallback.
5. **Security & Authentication**:
   - Argon2id password hashing and signed JWT authentication.
   - HttpOnly, SameSite, Secure cookie delivery with credentials CORS protection.
6. **PART 2 AI Integration Readiness**:
   - Pluggable AI provider architecture (`mock` and `openai`).
   - Prepared modules and API contracts for Legal RAG, summarization, citation graphs, and case similarity.

---

## 2. Technology Stack

- **Frontend**: React 18, TypeScript (strict mode), Vite, Tailwind CSS, Lucide React icons, React Router DOM, Zod.
- **Backend**: Python 3.12, FastAPI, Pydantic v2, Pydantic Settings, SQLAlchemy 2.x, Alembic, PostgreSQL with pgvector, PyMuPDF, python-docx, Pytest, Uvicorn.
- **Deployment**: Vercel Dual-Project architecture (Vite SPA on Frontend, Serverless Python Functions on Backend), Neon PostgreSQL with pgvector, Vercel Blob private storage.
- **No Docker**: Zero Docker dependencies; native runtime execution with virtual environments and npm.

---

## 3. Project Directory Structure

```text
nyayasetu-ai/
├── README.md
├── .gitignore
├── .env.example
├── .python-version
├── Makefile
├── docs/
│   ├── architecture.md
│   ├── api-reference.md
│   ├── dataset-import.md
│   ├── deployment-vercel.md
│   └── security-and-privacy.md
├── data/
│   ├── demo/
│   │   └── sample_judgments.json
│   └── import-reports/
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── vercel.json
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── routes/
│       ├── layouts/
│       ├── pages/
│       ├── components/
│       ├── hooks/
│       ├── lib/
│       └── types/
└── backend/
    ├── requirements.txt
    ├── pyproject.toml
    ├── index.py
    ├── vercel.json
    ├── alembic.ini
    ├── alembic/
    ├── app/
    │   ├── main.py
    │   ├── core/
    │   ├── db/
    │   ├── api/v1/
    │   ├── models/
    │   ├── schemas/
    │   ├── services/
    │   └── tests/
    └── scripts/
        ├── init_db.py
        ├── seed_demo.py
        ├── inspect_huggingface_dataset.py
        ├── import_huggingface_cases.py
        └── index_judgment_text.py
```

---

## 4. Local Development Quickstart

### Prerequisites
- Node.js (v18+) and npm
- Python 3.11 or 3.12

### Step 1: Backend Setup
```bash
cd backend
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database tables and seed demo advocate & judgments
python scripts/init_db.py
python scripts/seed_demo.py

# Start local FastAPI backend (runs on http://127.0.0.1:8000)
uvicorn app.main:app --reload --port 8000
```

### Step 2: Frontend Setup
In a new terminal:
```bash
cd frontend
npm install
npm run dev
# React Vite application runs on http://127.0.0.1:5173
```

### Demo Login Credentials
- **Email**: `advocate@nyayasetu.ai`
- **Password**: `NyayaSetu@2026`

---

## 5. Hugging Face Dataset Commands

```bash
cd backend

# 1. Inspect Hugging Face dataset schema & configurations
python scripts/inspect_huggingface_dataset.py

# 2. Test import with a dry run (no DB writes)
python scripts/import_huggingface_cases.py --limit 100 --dry-run

# 3. Batch import 100 case laws idempotently
python scripts/import_huggingface_cases.py --limit 100 --batch-size 50

# 4. Chunk & index indexable judgment text
python scripts/index_judgment_text.py --limit 100
```

---

## 6. Testing & Validation

```bash
# Run backend test suite
cd backend
python -m pytest app/tests -v

# Typecheck and build frontend for production
cd frontend
npm run build
```

---

## 7. Legal Safety Disclaimer

NyayaSetu AI is an independent technological platform built to streamline court case tracking and legal research. It does not provide judicial adjudication, calculate definitive win probabilities, or replace professional legal representation by licensed advocates.

