"""
Application configuration using Pydantic Settings.
Safe defaults allow startup even if some environment variables are omitted.
"""
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    # General
    PROJECT_NAME: str = "NyayaSetu AI"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # Security & Auth
    JWT_SECRET_KEY: str = "dev-insecure-secret-key-replace-in-production-min-32-chars"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours default in dev

    # CORS & Origins
    FRONTEND_URL: str = "http://localhost:5173"
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    @property
    def cors_origins(self) -> List[str]:
        origins = [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]
        if self.FRONTEND_URL and self.FRONTEND_URL not in origins:
            origins.append(self.FRONTEND_URL)
        return origins

    # Database
    DATABASE_URL: Optional[str] = None
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    # Document Upload Limits & Storage
    MAX_UPLOAD_SIZE_MB: int = 4
    BLOB_READ_WRITE_TOKEN: Optional[str] = None
    LOCAL_STORAGE_DIR: str = "storage/documents"

    # AI Provider Configuration (Part 2 Integration Points)
    AI_PROVIDER: str = "mock"
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIMENSION: int = 1536

    # Hugging Face Dataset Defaults
    HF_DATASET_ID: str = "Sumitedu/indian-case-laws"
    HF_DATASET_CONFIG: Optional[str] = None
    HF_DATASET_SPLIT: str = "train"
    HF_DATASET_STREAMING: bool = True
    HF_IMPORT_LIMIT: int = 100
    HF_IMPORT_BATCH_SIZE: int = 100
    HF_IMPORT_RESUME: bool = True

    # Text Indexing Defaults
    HF_INDEXING_LIMIT: int = 100
    HF_INDEXING_BATCH_SIZE: int = 25

    # Demo / Seed
    SEED_DEMO_DATA: bool = False


settings = Settings()

