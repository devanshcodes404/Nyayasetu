# Vercel Dual-Project Deployment Guide

NyayaSetu AI is designed for seamless Git-based deployment on Vercel without Docker. The repository contains two independently deployable roots connected to a single PostgreSQL database with pgvector.

---

## 1. Managed PostgreSQL & pgvector Setup

1. **Create Managed Database**:
   - Provision a PostgreSQL database via **Neon** (or Vercel Marketplace PostgreSQL).
2. **Enable pgvector**:
   - In Neon SQL Editor, execute:
     ```sql
     CREATE EXTENSION IF NOT EXISTS vector;
     ```
3. **Copy Pooled Connection String**:
   - Copy the connection URL formatted as `postgresql://<user>:<password>@<host>/<dbname>?sslmode=require`.

---

## 2. Project A — NyayaSetu AI Frontend

1. Go to **Vercel Dashboard > New Project** and import the repository.
2. In Project Settings:
   - **Project Name**: `nyayasetu-ai-frontend`
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. Configure Environment Variables:
   - `VITE_API_BASE_URL`: `https://nyayasetu-ai-backend.vercel.app/api/v1` (URL of deployed Project B)
4. Deploy the project. The SPA rewrite rules in `frontend/vercel.json` ensure direct URL navigation works correctly.

---

## 3. Project B — NyayaSetu AI Backend

1. In Vercel Dashboard, import the **same repository** as a second project.
2. In Project Settings:
   - **Project Name**: `nyayasetu-ai-backend`
   - **Framework Preset**: `Other`
   - **Root Directory**: `backend`
   - **Output Directory**: Leave empty
3. Configure Environment Variables:
   - `DATABASE_URL`: Your pooled PostgreSQL connection string from Neon.
   - `JWT_SECRET_KEY`: A 64-character random hex key (`openssl rand -hex 32`).
   - `FRONTEND_URL`: `https://nyayasetu-ai-frontend.vercel.app` (URL of deployed Project A).
   - `ALLOWED_ORIGINS`: `https://nyayasetu-ai-frontend.vercel.app`
   - `ENVIRONMENT`: `production`
   - `MAX_UPLOAD_SIZE_MB`: `4`
   - `BLOB_READ_WRITE_TOKEN`: (Optional) Vercel Blob access token for private document storage.
   - `AI_PROVIDER`: `mock`
4. Deploy the project. `backend/index.py` will serve the FastAPI application as a serverless function.

---

## 4. Applying Database Migrations to Production

From your local machine or an external deployment pipeline, run the Alembic migrations pointing to the managed database:

```bash
cd backend
export DATABASE_URL="postgresql://<user>:<password>@<host>/<dbname>?sslmode=require"
python scripts/init_db.py
alembic upgrade head
```

Verify backend health at:
`https://nyayasetu-ai-backend.vercel.app/api/v1/health`

