"""Funções de processamento e agregação meteorológica."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from f1.domain.models import Weather, WeatherSummary


def summarize_weather(weather_list: list[Weather]) -> WeatherSummary | None:
    """Calcula estatísticas de clima (mínimo, máximo, médias e valores recentes)."""
    from f1.domain.models import WeatherSummary

    if not weather_list:
        return None

    air_temps = [
        w.air_temperature for w in weather_list if w.air_temperature is not None
    ]
    track_temps = [
        w.track_temperature for w in weather_list if w.track_temperature is not None
    ]
    humidities = [w.humidity for w in weather_list if w.humidity is not None]
    rain = any(bool(w.rainfall and w.rainfall > 0) for w in weather_list)

    last = weather_list[-1]

    return WeatherSummary(
        air_temp_min=min(air_temps) if air_temps else None,
        air_temp_max=max(air_temps) if air_temps else None,
        track_temp_min=min(track_temps) if track_temps else None,
        track_temp_max=max(track_temps) if track_temps else None,
        humidity_avg=round(sum(humidities) / len(humidities), 1)
        if humidities
        else None,
        rainfall=rain,
        air_temp_last=last.air_temperature,
        track_temp_last=last.track_temperature,
        humidity_last=last.humidity,
    )
