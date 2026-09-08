from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "CareerPulse API"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # Database Settings
    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "career_db"
    POSTGRES_PORT: int = 5432

    # Redis & Celery
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_URL: str
    
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    # LOCAL FILE STORAGE
    LOCAL_STORAGE_DIR: str = "storage/documents"

    # Jina AI Embeddings v3
    JINA_API_KEY: str
    JINA_EMBEDDING_MODEL: str = "jina-embeddings-v3"
    JINA_EMBEDDING_DIMENSION: int = 1024
    JINA_PASSAGE_TASK: str = "retrieval.passage"
    JINA_QUERY_TASK: str = "retrieval.query"

    # Groq LLM
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()