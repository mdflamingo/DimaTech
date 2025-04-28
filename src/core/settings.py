import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # поднимаемся на 3 уровня вверх


class Settings(BaseSettings):
    postgres_db: str
    db_port: int
    db_host: str
    postgres_user: str
    postgres_password: str

    secret_key: str

    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False
    )


settings = Settings()  # type: ignore
