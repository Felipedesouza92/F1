"""Modelos Pydantic que espelham os payloads da OpenF1 API.

Inclui também projeções produzidas pela camada de processing.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Meeting(BaseModel):
    """Fim de semana de corrida (GP)."""

    model_config = ConfigDict(extra="ignore")

    meeting_key: int
    meeting_name: str
    country_name: str | None = None
    circuit_short_name: str | None = None
    year: int
    date_start: str | None = None


class Session(BaseModel):
    """Sessão dentro de um meeting (Treino, Quali, Sprint, Corrida)."""

    model_config = ConfigDict(extra="ignore")

    session_key: int
    meeting_key: int
    session_name: str
    session_type: str | None = None
    date_start: str | None = None
    date_end: str | None = None
    year: int


class Driver(BaseModel):
    """Piloto participante de uma sessão."""

    model_config = ConfigDict(extra="ignore")

    driver_number: int
    full_name: str | None = None
    name_acronym: str | None = None
    team_name: str | None = None
    team_colour: str | None = None
    headshot_url: str | None = None


class Lap(BaseModel):
    """Dados de uma volta individual."""

    model_config = ConfigDict(extra="ignore")

    driver_number: int
    lap_number: int
    lap_duration: float | None = None
    duration_sector_1: float | None = None
    duration_sector_2: float | None = None
    duration_sector_3: float | None = None
    i1_speed: float | None = None
    i2_speed: float | None = None
    st_speed: float | None = None
    is_pit_out_lap: bool = False


class Stint(BaseModel):
    """Stint de pneu de um piloto."""

    model_config = ConfigDict(extra="ignore")

    driver_number: int
    stint_number: int
    compound: str | None = None
    lap_start: int | None = None
    lap_end: int | None = None
    tyre_age_at_start: int | None = None


class PitStop(BaseModel):
    """Evento de pit stop."""

    model_config = ConfigDict(extra="ignore")

    driver_number: int
    lap_number: int | None = None
    pit_duration: float | None = None


class SessionResult(BaseModel):
    """Resultado de um piloto em uma sessão.

    Na corrida, `gap_to_leader` é escalar.
    Na quali, `gap_to_leader` pode ser uma lista (Q1, Q2, Q3).
    """

    model_config = ConfigDict(extra="ignore")

    driver_number: int
    position: int | None = None


class Weather(BaseModel):
    """Condição meteorológica em um instante."""

    model_config = ConfigDict(extra="ignore")

    date: str | None = None
    air_temperature: float | None = None
    track_temperature: float | None = None
    humidity: float | None = None
    rainfall: int | None = None
    wind_speed: float | None = None
    wind_direction: int | None = None


# ───────────────────────────── Projeções do processing ─────────────────────────


class FastestLapEntry(BaseModel):
    """Melhor volta de um piloto com setores."""

    driver_number: int
    driver_name: str
    team_name: str
    team_colour: str
    lap_duration: float
    sector_1: float | None = None
    sector_2: float | None = None
    sector_3: float | None = None


class StintBar(BaseModel):
    """Stint para visualização em barras horizontais."""

    driver_number: int
    driver_name: str
    compound: str
    lap_start: int
    lap_end: int


class PitSummary(BaseModel):
    """Resumo de pit stop para exibição."""

    driver_number: int
    driver_name: str
    lap_number: int | None = None
    pit_duration: float | None = None


class WeatherSummary(BaseModel):
    """Resumo do clima da sessão."""

    air_temp_min: float | None = None
    air_temp_max: float | None = None
    track_temp_min: float | None = None
    track_temp_max: float | None = None
    humidity_avg: float | None = None
    rainfall: bool = False
    air_temp_last: float | None = None
    track_temp_last: float | None = None
    humidity_last: float | None = None


class ClassificationEntry(BaseModel):
    """Entrada na classificação de uma sessão."""

    position: int | None = None
    driver_number: int
    driver_name: str
    team_name: str
    team_colour: str
    status: str = ""


class SessionOverview(BaseModel):
    """Agrega tudo o que a tela da sessão precisa."""

    drivers: list[Driver] = []
    classification: list[ClassificationEntry] = []
    fastest_laps: list[FastestLapEntry] = []
    stint_timeline: list[StintBar] = []
    pit_stops: list[PitSummary] = []
    weather: WeatherSummary | None = None

