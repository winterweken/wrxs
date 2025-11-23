from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://wrxs_user:wrxs_password@postgres:5432/wrxs"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # OpenAI (optional for AI features)
    OPENAI_API_KEY: Optional[str] = None

    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost"]

    class Config:
        env_file = ".env"


settings = Settings()
