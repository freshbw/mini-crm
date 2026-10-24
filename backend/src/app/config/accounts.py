import tomllib
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel


class SecretRef(BaseModel):
    secret: str


class TelegramConfig(BaseModel):
    bot_token: SecretRef | str


class EmailConfig(BaseModel):
    imap_host: str
    imap_port: int = 993
    imap_user: str
    imap_password: SecretRef | str
    smtp_host: str
    smtp_port: int = 587
    smtp_user: str
    smtp_password: SecretRef | str


class Accounts(BaseModel):
    telegram: TelegramConfig
    email: EmailConfig


def _secret(ref: SecretRef | str) -> str:
    if isinstance(ref, str):
        return ref
    return (Path("secrets") / ref.secret).read_text(encoding="utf-8").strip()


@lru_cache
def get_accounts() -> Accounts:
    raw = tomllib.loads(Path("config/accounts.toml").read_text(encoding="utf-8"))
    acc = Accounts.model_validate(raw)
    acc.telegram.bot_token = _secret(acc.telegram.bot_token)
    acc.email.imap_password = _secret(acc.email.imap_password)
    acc.email.smtp_password = _secret(acc.email.smtp_password)
    return acc
