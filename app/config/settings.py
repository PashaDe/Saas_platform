from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/app"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "change-me"
    encryption_key: str | None = None
    postgres_password: str | None = None
    postgres_sync_url: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()


