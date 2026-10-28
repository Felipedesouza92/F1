"""Testes unitários para o módulo utils/config.py."""

from f1.utils.config import Settings, load_settings


def test_settings_default_values():
    settings = Settings()
    assert settings.base_url == "https://api.openf1.org/v1"
    assert settings.timeout == 10
    assert settings.environment == "development"
    assert settings.cache_ttl_seconds == 3600


def test_settings_production_ttl():
    settings = Settings(environment="production")
    assert settings.cache_ttl_seconds == 86400


def test_load_settings(monkeypatch):
    monkeypatch.setenv("OPENF1_BASE_URL", "https://custom.api.org")
    monkeypatch.setenv("OPENF1_TIMEOUT", "15")
    monkeypatch.setenv("ENVIRONMENT", "staging")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    settings = load_settings()
    assert settings.base_url == "https://custom.api.org"
    assert settings.timeout == 15
    assert settings.environment == "staging"
    assert settings.log_level == "DEBUG"
    assert settings.cache_ttl_seconds == 86400

