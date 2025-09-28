import os
from dataclasses import dataclass


@dataclass
class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@postgres:5432/app"
    )
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    secret_key: str = os.getenv("SECRET_KEY", "change-me")
    encryption_key: str | None = os.getenv("ENCRYPTION_KEY")
    postgres_password: str | None = os.getenv("POSTGRES_PASSWORD")
    postgres_sync_url: str | None = os.getenv("POSTGRES_SYNC_URL")


settings = Settings()


