"""Testes unitários para geração de figuras do Plotly."""

import plotly.graph_objects as go

from f1.dashboard.charts import fastest_laps_bar, pace_lines, stint_timeline
from f1.domain.models import FastestLapEntry, StintBar


def test_fastest_laps_bar_empty():
    fig = fastest_laps_bar([])
    assert isinstance(fig, go.Figure)


def test_fastest_laps_bar_with_data():
    entries = [
        FastestLapEntry(
            driver_number=1,
            driver_name="Verstappen",
            team_name="Red Bull",
            team_colour="#3671C6",
            lap_duration=83.5,
        )
    ]
    fig = fastest_laps_bar(entries)
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1


def test_pace_lines():
    series = {1: [(1, 85.0), (2, 84.5)]}
    names = {1: "Verstappen"}
    colors = {1: "#3671C6"}
    fig = pace_lines(series, names, colors)
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1


def test_stint_timeline():
    stints = [
        StintBar(
            driver_number=1,
            driver_name="Verstappen",
            compound="SOFT",
            lap_start=1,
            lap_end=15,
        )
    ]
    fig = stint_timeline(stints)
    assert isinstance(fig, go.Figure)
    assert len(fig.data) >= 1
