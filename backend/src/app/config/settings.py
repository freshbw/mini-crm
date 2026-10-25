import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, SecretStr
from pydantic_settings import (
    BaseSettings,
    NestedSecretsSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

BASE_DIR = Path(__file__).resolve().parents[4]
SECRETS_DIR = Path(os.getenv("SECRETS_DIR", BASE_DIR / "secrets"))
TOML_FILE = BASE_DIR / "config" / "accounts.toml"


class PostgresSettings(BaseModel):
    user: str = "minicrm"
    host: str = "localhost"
    password: SecretStr
    db: str = "minicrm"
    port: int = 5432


class ValkeySettings(BaseModel):
    host: str = "localhost"
    port: int = 6379
    password: SecretStr


class TelegramSettings(BaseModel):
    bot_token: SecretStr


class SmtpSettings(BaseModel):
    host: str
    port: int = 587
    user: str
    password: SecretStr


class ImapSettings(BaseModel):
    host: str
    port: int = 993
    user: str
    password: SecretStr


class EmailSettings(BaseModel):
    smtp: SmtpSettings
    imap: ImapSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        secrets_dir=SECRETS_DIR,
        toml_file=TOML_FILE,
        extra="ignore",
    )

    postgres: PostgresSettings
    valkey: ValkeySettings
    email: EmailSettings
    telegram: TelegramSettings

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            NestedSecretsSettingsSource(file_secret_settings),
            TomlConfigSettingsSource(settings_cls),
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
