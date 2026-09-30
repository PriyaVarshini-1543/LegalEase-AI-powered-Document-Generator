from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LegalEase"
    app_version: str = "1.0.0"
    openai_api_key: str | None = None
    openai_model: str = "gpt-5-mini"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    frontend_api_url: str = "http://127.0.0.1:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
