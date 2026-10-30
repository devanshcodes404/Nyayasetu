# Architecture Specification — NyayaSetu AI

NyayaSetu AI is an enterprise-grade, cloud-native legal technology platform engineered for Indian advocates, law firms, and legal researchers.

## 1. High-Level System Architecture

NyayaSetu AI is built on a decoupled full-stack architecture designed for deployment on Vercel without Docker:

```
┌────────────────────────────────────────────────────────┐
│               Frontend: React 18 + Vite               │
│  (Tailwind CSS, React Router, Lucide, TypeScript)     │
└──────────────────────────┬─────────────────────────────┘
                           │ HTTPS / JSON / Cookies
                           ▼
┌────────────────────────────────────────────────────────┐
│               Backend: FastAPI Python 3.12            │
│ (index.py Vercel Function / Uvicorn Serverless Handler)│
└────────────┬─────────────┬─────────────┬───────────────┘
             │             │             │
             ▼             ▼             ▼
┌─────────────────┐ ┌─────────────┐ ┌───────────────────┐
│   PostgreSQL    │ │ Vercel Blob │ │  AI Integration   │
│   + pgvector    │ │   Storage   │ │   (PART 2 Ready)  │
│(Neon Serverless)│ │  (Private)  │ │ (Mock & OpenAI)   │
└─────────────────┘ └─────────────┘ └───────────────────┘
```

## 2. Component Boundaries & Responsibilities

### 2.1 React Frontend (`frontend/`)
- Pure client-side SPA bundle built with Vite and React 18 in TypeScript strict mode.
- Deployed as Project A on Vercel with automatic SPA rewrites (`vercel.json`).
- Communicates exclusively through typed HTTP requests to the FastAPI backend API via `api-client.ts`.
- Manages authenticated session states via HttpOnly cookies and credentials-bearing requests.

### 2.2 FastAPI Backend (`backend/`)
- High-performance asynchronous API server built on Python 3.12.
- Deployed as Project B on Vercel Serverless Functions via `backend/index.py`.
- Stateless request processing with Argon2 password hashing and signed JWT authentication tokens.
- Strict multi-tenancy: user briefs and uploaded files are isolated by `owner_id`.
- Parameterized database-backed search for public case-law without requiring expensive upfront vector embeddings.

### 2.3 Database Tier (PostgreSQL + pgvector)
- Managed PostgreSQL (Neon serverless or Vercel Marketplace PostgreSQL).
- Alembic database migrations tracking schema evolution.
- Stores users, private case briefs, document metadata, public judgments, chunks, citations, and import jobs.
- Composite uniqueness constraints (`source_dataset`, `external_id`) preventing duplicates.

### 2.4 Document Storage & Text Ingestion
- User documents uploaded via `POST /api/v1/documents/upload`.
- Checksummed using SHA-256 and text-extracted via PyMuPDF (PDF), python-docx (DOCX), and raw text parsers.
- Scanned PDF detection flagging documents requiring OCR.
- Durable storage via Vercel Blob private tokens (production) or local disk adapter (development).

### 2.5 Hugging Face Dataset Pipeline (`Sumitedu/indian-case-laws`)
- External batch pipeline decoupled from serverless HTTP handlers.
- Executed via CLI scripts (`inspect_huggingface_dataset.py`, `import_huggingface_cases.py`, `index_judgment_text.py`).
- Idempotent, resumable, and transactional batch loading.

