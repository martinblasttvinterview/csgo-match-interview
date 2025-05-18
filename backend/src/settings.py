import pathlib

from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict

DOTENV = pathlib.Path(__file__).parent.parent / ".env"


class BaseSettings(PydanticBaseSettings):
    """Base settings."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class Settings(BaseSettings):
    """Main settings."""

    env: str = "local"
    host: str = "localhost"
    port: int = 8000
    workers: int = 1
    log_level: str = "info"
    reload: bool = True

    model_config = SettingsConfigDict(
        env_file=DOTENV,
    )


settings = Settings()
