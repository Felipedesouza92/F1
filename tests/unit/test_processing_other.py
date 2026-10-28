"""Testes unitários para o processamento meteorológico e stints."""

from f1.domain.models import Driver, PitStop, Stint, Weather
from f1.processing.laps import build_driver_index
from f1.processing.stints import build_stint_timeline, pit_summary
from f1.processing.weather import summarize_weather


def test_summarize_weather():
    w_empty = summarize_weather([])
    assert w_empty is None

    w_list = [
        Weather(
            air_temperature=25.0, track_temperature=35.0, humidity=50.0, rainfall=0
        ),
        Weather(
            air_temperature=27.0, track_temperature=40.0, humidity=55.0, rainfall=1
        ),
    ]
    summary = summarize_weather(w_list)
    assert summary is not None
    assert summary.air_temp_min == 25.0
    assert summary.air_temp_max == 27.0
    assert summary.track_temp_max == 40.0
    assert summary.rainfall is True
    assert summary.air_temp_last == 27.0


def test_stints_and_pits():
    drivers = [Driver(driver_number=44, full_name="Lewis Hamilton")]
    index = build_driver_index(drivers)

    stints = [
        Stint(
            driver_number=44, stint_number=1, compound="medium", lap_start=1, lap_end=20
        )
    ]
    timeline = build_stint_timeline(stints, index)
    assert len(timeline) == 1
    assert timeline[0].compound == "MEDIUM"

    pits = [PitStop(driver_number=44, lap_number=20, pit_duration=22.4)]
    res = pit_summary(pits, index)
    assert len(res) == 1
    assert res[0].pit_duration == 22.4
