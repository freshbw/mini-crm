from functools import lru_cache
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    postgres_user: str = "minicrm"
    postgres_host: str = "localhost"
    postgres_password: str | None = None
    postgres_db: str = "minicrm"
    postgres_port: int = 5432

    valkey_host: str = "localhost"
    valkey_port: int = 6379
    valkey_password: str | None = None

    @property
    def database_url(self) -> str:
        if self.postgres_password:
            return (
                f"postgresql+asyncpg://{self.postgres_user}:{quote_plus(self.postgres_password)}"
                f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
            )
        return (
            f"postgresql+asyncpg://{self.postgres_user}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def valkey_url(self) -> str:
        if self.valkey_password:
            return f"redis://:{quote_plus(self.valkey_password)}@{self.valkey_host}:{self.valkey_port}/0"
        return f"redis://{self.valkey_host}:{self.valkey_port}/0"


@lru_cache
def get_settings() -> Settings:
    return Settings()
