from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "Face Recognition Service"
    api_prefix: str = "/api/v1"
    database_url: str | None = None
    embeddings_cache_refresh_seconds: int = 300
    allowed_origins: List[AnyHttpUrl] = []

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()

