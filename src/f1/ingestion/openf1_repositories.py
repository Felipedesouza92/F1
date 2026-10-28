"""Implementações concretas dos repositórios OpenF1."""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from f1.domain.models import (
    Driver,
    Lap,
    Meeting,
    PitStop,
    Session,
    SessionResult,
    Stint,
    Weather,
)
from f1.domain.repositories import (
    DriverRepository,
    LapRepository,
    MeetingRepository,
    PitRepository,
    SessionRepository,
    SessionResultRepository,
    StintRepository,
    WeatherRepository,
)
from f1.ingestion.http_client import HttpClient
from f1.utils.logger import get_logger

logger = get_logger(__name__)


def _parse_items(raw_list: list[dict[str, Any]], model_cls: Any) -> list[Any]:
    valid = []
    ignored = 0
    for item in raw_list:
        try:
            valid.append(model_cls.model_validate(item))
        except ValidationError:
            ignored += 1
    if ignored > 0:
        logger.warning(
            "Ignorados %d itens inválidos ao parsear para %s",
            ignored,
            model_cls.__name__,
        )
    return valid


class OpenF1MeetingRepository(MeetingRepository):
    """Repositório de reuniões/GPs."""

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def list(self, year: int) -> list[Meeting]:
        """Lista meetings de um ano."""
        raw = self._client.get("meetings", {"year": year})
        return _parse_items(raw, Meeting)


class OpenF1SessionRepository(SessionRepository):
    """Repositório de sessões."""

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def list(self, meeting_key: int) -> list[Session]:
        """Lista sessões de um meeting."""
        raw = self._client.get("sessions", {"meeting_key": meeting_key})
        return _parse_items(raw, Session)


class OpenF1DriverRepository(DriverRepository):
    """Repositório de pilotos."""

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def list(self, session_key: int) -> list[Driver]:
        """Lista pilotos de uma sessão."""
        raw = self._client.get("drivers", {"session_key": session_key})
        return _parse_items(raw, Driver)


class OpenF1LapRepository(LapRepository):
    """Repositório de voltas."""

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def list(self, session_key: int, driver_number: int | None = None) -> list[Lap]:
        """Lista voltas de uma sessão."""
        params: dict[str, Any] = {"session_key": session_key}
        if driver_number is not None:
            params["driver_number"] = driver_number
        raw = self._client.get("laps", params)
        return _parse_items(raw, Lap)


class OpenF1StintRepository(StintRepository):
    """Repositório de stints."""

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def list(self, session_key: int) -> list[Stint]:
        """Lista stints de uma sessão."""
        raw = self._client.get("stints", {"session_key": session_key})
        return _parse_items(raw, Stint)


class OpenF1PitRepository(PitRepository):
    """Repositório de pit stops."""

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def list(self, session_key: int) -> list[PitStop]:
        """Lista pit stops de uma sessão."""
        raw = self._client.get("pit", {"session_key": session_key})
        return _parse_items(raw, PitStop)


class OpenF1SessionResultRepository(SessionResultRepository):
    """Repositório de resultados da sessão."""

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def list(self, session_key: int) -> list[SessionResult]:
        """Lista resultados de uma sessão."""
        raw = self._client.get("position", {"session_key": session_key})
        return _parse_items(raw, SessionResult)


class OpenF1WeatherRepository(WeatherRepository):
    """Repositório de dados meteorológicos."""

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def list(self, session_key: int) -> list[Weather]:
        """Lista medições meteorológicas de uma sessão."""
        raw = self._client.get("weather", {"session_key": session_key})
        return _parse_items(raw, Weather)
