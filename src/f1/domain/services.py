"""Serviço de orquestração do F1 Dashboard.

Recebe repositórios por injeção e delega o processamento para funções puras.
"""

from f1.domain.models import Meeting, Session, SessionOverview
from f1.domain.repositories import (
    DriverRepository,
    LapRepository,
    MeetingRepository,
    PitRepository,
    SessionRepository,
    StintRepository,
    WeatherRepository,
)
from f1.processing.laps import build_driver_index, compute_top_n_laps
from f1.processing.results import build_classification
from f1.processing.stints import build_stint_timeline, pit_summary
from f1.processing.weather import summarize_weather
from f1.utils.logger import get_logger

logger = get_logger(__name__)


class F1DashboardService:
    """Serviço principal que orquestra as chamadas aos repositórios."""

    def __init__(
        self,
        meetings: MeetingRepository,
        sessions: SessionRepository,
        drivers: DriverRepository,
        laps: LapRepository,
        stints: StintRepository,
        pits: PitRepository,
        weather: WeatherRepository,
    ) -> None:
        """Inicializa o serviço com repositórios injetados."""
        self._meetings = meetings
        self._sessions = sessions
        self._drivers = drivers
        self._laps = laps
        self._stints = stints
        self._pits = pits
        self._weather = weather

    def list_meetings(self, year: int) -> list[Meeting]:
        """Lista meetings de um ano, ordenados por data."""
        meetings = self._meetings.list(year)
        return sorted(meetings, key=lambda m: m.date_start or "")

    def list_sessions(self, meeting_key: int) -> list[Session]:
        """Lista sessões de um meeting."""
        return self._sessions.list(meeting_key)

    def get_session_overview(
        self, session_key: int, top_n: int = 10
    ) -> SessionOverview:
        """Monta a visão completa de uma sessão para o dashboard."""
        logger.info("Montando overview da sessão %d", session_key)

        drivers = self._drivers.list(session_key)
        driver_index = build_driver_index(drivers)

        laps = self._laps.list(session_key)
        fastest = compute_top_n_laps(laps, driver_index, top_n)

        stints = self._stints.list(session_key)
        timeline = build_stint_timeline(stints, driver_index)

        pits = self._pits.list(session_key)
        pit_stops = pit_summary(pits, driver_index)

        weather_data = self._weather.list(session_key)
        weather_sum = summarize_weather(weather_data)

        classification = build_classification(drivers, driver_index)

        return SessionOverview(
            drivers=drivers,
            classification=classification,
            fastest_laps=fastest,
            stint_timeline=timeline,
            pit_stops=pit_stops,
            weather=weather_sum,
        )
