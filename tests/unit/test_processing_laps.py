"""Testes unitários para processamento de voltas."""

from f1.domain.models import Driver, Lap
from f1.processing.laps import (
    build_driver_index,
    compute_top_n_laps,
    filter_valid_laps,
    lap_time_series,
)


def test_filter_valid_laps():
    laps = [
        Lap(driver_number=1, lap_number=1, lap_duration=None),
        Lap(driver_number=1, lap_number=2, lap_duration=85.0, is_pit_out_lap=True),
        Lap(driver_number=1, lap_number=3, lap_duration=84.5, is_pit_out_lap=False),
        Lap(driver_number=1, lap_number=4, lap_duration=0.0, is_pit_out_lap=False),
    ]
    valid = filter_valid_laps(laps)
    assert len(valid) == 1
    assert valid[0].lap_number == 3


def test_compute_top_n_laps():
    drivers = [
        Driver(driver_number=1, full_name="Max Verstappen", team_name="Red Bull", team_colour="3671C6"),
        Driver(driver_number=44, full_name="Lewis Hamilton", team_name="Mercedes", team_colour="6CD3BF"),
    ]
    index = build_driver_index(drivers)

    laps = [
        Lap(driver_number=1, lap_number=5, lap_duration=84.0),
        Lap(driver_number=1, lap_number=6, lap_duration=83.5),
        Lap(driver_number=44, lap_number=10, lap_duration=83.8),
    ]

    top = compute_top_n_laps(laps, index, n=10)
    assert len(top) == 2
    assert top[0].driver_number == 1
    assert top[0].lap_duration == 83.5
    assert top[0].team_colour == "#3671C6"
    assert top[1].driver_number == 44
    assert top[1].lap_duration == 83.8


def test_lap_time_series_removes_outliers():
    laps = [
        Lap(driver_number=1, lap_number=1, lap_duration=80.0),
        Lap(driver_number=1, lap_number=2, lap_duration=81.0),
        Lap(driver_number=1, lap_number=3, lap_duration=80.5),
        Lap(driver_number=1, lap_number=4, lap_duration=120.0),  # Outlier (Safety car / Pit in)
    ]
    series = lap_time_series(laps, [1])
    assert 1 in series
    lap_numbers = [p[0] for p in series[1]]
    assert 4 not in lap_numbers
    assert len(lap_numbers) == 3

