# Security and Privacy Architecture

## 1. Authentication & Session Security
- **Argon2id Password Hashing**: Passwords are never stored in plaintext. They are hashed using Argon2id with memory cost and time cost protections against GPU brute-force attacks.
- **Signed JWT Tokens**: Tokens are generated using HMAC-SHA256 with strong secrets (`JWT_SECRET_KEY`) and configured expiration.
- **HttpOnly Cookies**: Session tokens are placed inside HttpOnly, SameSite=Lax, Secure cookies to mitigate Cross-Site Scripting (XSS) token theft.
- **Origin Validation**: Strict CORS origin whitelisting prevents cross-origin abuse.

## 2. Multi-Tenancy & Resource Ownership
- **Strict User Isolation**: All private cases and legal documents enforce `owner_id == current_user.id` on every database query, update, and deletion.
- **Public vs. Private Separation**: Public judgments from Hugging Face corpus are stored in a dedicated `judgments` table with no tenant ownership or workspace mixing. Private user documents are stored in `documents` with strict ownership foreign keys.

## 3. Document Privacy & Storage Security
- **Vercel Blob Private Storage**: User documents are stored under random UUID keys. Direct access URLs are never exposed publicly; file downloads are authenticated through backend endpoints.
- **File Validation**: MIME types, binary file headers, and SHA-256 checksums are verified before ingestion. File uploads are strictly size-capped (`MAX_UPLOAD_SIZE_MB`).

## 4. Legal Integrity & Disclaimers
- NyayaSetu AI is an independent software tool designed to assist legal research and case administration.
- It is **not** an official court filing portal and does not possess government affiliation.
- Historical outcome analytics are informational only and never claim to guarantee court outcomes.

