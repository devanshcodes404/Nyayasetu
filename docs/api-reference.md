# NyayaSetu AI API Reference

Base URL: `/api/v1`  
OpenAPI Documentation: `/api/docs`  
ReDoc Documentation: `/api/redoc`

All authenticated endpoints require an `Authorization: Bearer <token>` header or a valid `nyayasetu_token` HttpOnly session cookie.

---

## 1. System Health

### `GET /api/v1/health`
Checks database connectivity and AI provider configuration.
- **Response**: `200 OK`
```json
{
  "status": "healthy",
  "service": "NyayaSetu AI Backend",
  "environment": "development",
  "database": "healthy",
  "ai_provider": "mock"
}
```

---

## 2. Authentication

### `POST /api/v1/auth/register`
Creates a new advocate user account and returns a JWT token.
- **Body**:
```json
{
  "full_name": "Advocate Priya Sharma",
  "email": "priya.sharma@example.com",
  "password": "SecurePassword123!"
}
```
- **Response**: `201 Created`

### `POST /api/v1/auth/login`
Authenticates credentials and sets the `nyayasetu_token` HttpOnly cookie.
- **Body**:
```json
{
  "email": "priya.sharma@example.com",
  "password": "SecurePassword123!"
}
```
- **Response**: `200 OK`

### `POST /api/v1/auth/logout`
Clears session cookies.
- **Response**: `200 OK`

### `GET /api/v1/auth/me`
Returns current authenticated user profile.
- **Response**: `200 OK`

---

## 3. Court Cases

### `GET /api/v1/cases`
Lists all case briefs owned by the current advocate. Supports `?status=` and `?q=` filtering.
- **Response**: `200 OK` (Array of `CaseResponse`)

### `POST /api/v1/cases`
Creates a new legal brief.
- **Body**:
```json
{
  "title": "State of Maharashtra v. Union of India",
  "case_number": "CA/4102/2021",
  "court": "Supreme Court of India",
  "jurisdiction": "Appellate",
  "case_type": "Constitutional",
  "client_name": "State of Maharashtra",
  "opposing_party": "Union of India & Ors.",
  "status": "Active",
  "filing_date": "2021-08-14",
  "next_hearing_date": "2026-11-15",
  "description": "Constitutional challenge under Article 163."
}
```
- **Response**: `201 Created`

### `GET /api/v1/cases/{case_id}`
Retrieves single brief. Returns `404 Not Found` if not owned by the user.

### `PATCH /api/v1/cases/{case_id}`
Updates brief fields.

### `DELETE /api/v1/cases/{case_id}`
Deletes brief and cascades associated documents.

---

## 4. Case Documents

### `GET /api/v1/documents`
Lists documents owned by the user. Optional `?case_id=`.

### `POST /api/v1/documents/upload`
Uploads and parses a PDF, DOCX, or TXT file (multipart/form-data).
- **Form Fields**: `file` (binary), `title` (string, optional), `case_id` (integer, optional).
- **Response**: `201 Created`

### `DELETE /api/v1/documents/{document_id}`
Removes document metadata and deletes physical file from storage.

---

## 5. Public Indian Case-Law Corpus

### `GET /api/v1/judgments/search`
Database-backed keyword and filter search.
- **Query Parameters**:
  - `q`: Free-text search term
  - `court`: Court filter (e.g. `Supreme Court`)
  - `year`: Decision year (e.g. `2023`)
  - `citation`: Citation search
  - `page`: Page number (default: 1)
  - `page_size`: Results per page (default: 20)
- **Response**: `200 OK` (Paginated response with `items`, `total`, `total_pages`)

### `GET /api/v1/judgments/{judgment_id}`
Returns complete judgment details, court metadata, citations, and indexable text.

---

## 6. Dataset Ingestion Pipeline

### `GET /api/v1/dataset/status`
Returns metrics on imported corpus size, text completeness status, and latest import job.

---

## 7. PART 2 AI Integration Points

### `POST /api/v1/research/ask`
Legal RAG question answering endpoint. Returns structured Part 2 readiness response.

### `GET /api/v1/judgments/{judgment_id}/summary`
Judgment summarization endpoint.

### `GET /api/v1/cases/{case_id}/similar`
Precedent and similar-case matching endpoint.

### `GET /api/v1/documents/{document_id}/citations`
Document citation extraction and verification endpoint.

### `GET /api/v1/analytics/outcomes`
Aggregated outcome statistics from public judgment records.

