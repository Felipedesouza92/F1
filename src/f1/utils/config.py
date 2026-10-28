"""Configuração centralizada do projeto F1 Dashboard.

Carrega variáveis de ambiente via python-dotenv e expõe um dataclass Settings.
Nada é lido na importação — os testes passam um ambiente controlado.
"""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Configurações da aplicação, carregadas uma vez no ponto de entrada."""

    base_url: str = "https://api.openf1.org/v1"
    timeout: int = 10
    environment: str = "development"
    log_level: str = "INFO"
    cache_ttl_seconds: int = field(init=False)

    def __post_init__(self) -> None:
        """Define o TTL do cache com base no ambiente."""
        ttl = 3600 if self.environment == "development" else 86400
        object.__setattr__(self, "cache_ttl_seconds", ttl)


def load_settings() -> Settings:
    """Carrega as configurações do ambiente (`.env` se existir)."""
    load_dotenv()
    return Settings(
        base_url=os.environ.get("OPENF1_BASE_URL", "https://api.openf1.org/v1"),
        timeout=int(os.environ.get("OPENF1_TIMEOUT", "10")),
        environment=os.environ.get("ENVIRONMENT", "development"),
        log_level=os.environ.get("LOG_LEVEL", "INFO"),
    )

