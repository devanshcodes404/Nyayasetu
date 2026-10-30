.PHONY: help install-backend install-frontend install dev-backend dev-frontend test-backend build-frontend inspect-dataset import-dataset lint-frontend

help:
	@echo "NyayaSetu AI Developer Commands"
	@echo "--------------------------------"
	@echo "make install-backend   - Install backend requirements in active virtual environment"
	@echo "make install-frontend  - Install frontend npm packages"
	@echo "make dev-backend       - Run FastAPI backend locally with Uvicorn on :8000"
	@echo "make dev-frontend      - Run React/Vite frontend on :5173"
	@echo "make test-backend      - Run pytest backend test suite"
	@echo "make build-frontend    - Typecheck and build frontend for production"
	@echo "make inspect-dataset   - Inspect Hugging Face indian-case-laws corpus"
	@echo "make import-dataset    - Run idempotent batch import of sample judgments"

install-backend:
	cd backend && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

dev-backend:
	cd backend && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

dev-frontend:
	cd frontend && npm run dev

test-backend:
	cd backend && pytest app/tests -v

build-frontend:
	cd frontend && npm run build

inspect-dataset:
	cd backend && python scripts/inspect_huggingface_dataset.py

import-dataset:
	cd backend && python scripts/import_huggingface_cases.py --limit 100

