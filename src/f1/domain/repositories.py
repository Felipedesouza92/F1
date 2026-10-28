"""ABCs de repositórios — uma por endpoint da OpenF1 API.

A camada de domínio define os contratos; a camada de ingestion os implementa.
"""

from abc import ABC, abstractmethod

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


class MeetingRepository(ABC):
    """Contrato para buscar meetings (GPs)."""

    @abstractmethod
    def list(self, year: int) -> list[Meeting]:
        """Lista meetings de um ano."""


class SessionRepository(ABC):
    """Contrato para buscar sessões de um meeting."""

    @abstractmethod
    def list(self, meeting_key: int) -> list[Session]:
        """Lista sessões de um meeting."""


class DriverRepository(ABC):
    """Contrato para buscar pilotos de uma sessão."""

    @abstractmethod
    def list(self, session_key: int) -> list[Driver]:
        """Lista pilotos de uma sessão."""


class LapRepository(ABC):
    """Contrato para buscar voltas de uma sessão."""

    @abstractmethod
    def list(self, session_key: int, driver_number: int | None = None) -> list[Lap]:
        """Lista voltas de uma sessão, opcionalmente filtradas por piloto."""


class StintRepository(ABC):
    """Contrato para buscar stints de uma sessão."""

    @abstractmethod
    def list(self, session_key: int) -> list[Stint]:
        """Lista stints de uma sessão."""


class PitRepository(ABC):
    """Contrato para buscar pit stops de uma sessão."""

    @abstractmethod
    def list(self, session_key: int) -> list[PitStop]:
        """Lista pit stops de uma sessão."""


class SessionResultRepository(ABC):
    """Contrato para buscar resultados de uma sessão."""

    @abstractmethod
    def list(self, session_key: int) -> list[SessionResult]:
        """Lista resultados de uma sessão."""


class WeatherRepository(ABC):
    """Contrato para buscar dados meteorológicos de uma sessão."""

    @abstractmethod
    def list(self, session_key: int) -> list[Weather]:
        """Lista dados meteorológicos de uma sessão."""
