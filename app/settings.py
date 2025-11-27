import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    database_url: str
    secret_key: str


def get_settings() -> Settings:
    """
    Recupera configurações básicas de ambiente.
    - DATABASE_URL: URL do SQLite por padrão (calcweb.sqlite na raiz do projeto).
    - SECRET_KEY: chave para sessão/flash.
    """
    base_dir = Path(__file__).resolve().parent.parent
    default_db = base_dir / "calcweb.sqlite"

    database_url = os.getenv("DATABASE_URL", f"sqlite:///{default_db}")
    secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")

    return Settings(database_url=database_url, secret_key=secret_key)
