"""Testes unitários para formatação e utilitários de exibição."""

from f1.processing.formatting import format_lap_time, format_team_color


def test_format_lap_time():
    assert format_lap_time(83.456) == "1:23.456"
    assert format_lap_time(59.999) == "0:59.999"
    assert format_lap_time(125.100) == "2:05.100"
    assert format_lap_time(None) == "--:--.---"
    assert format_lap_time(-5.0) == "--:--.---"


def test_format_team_color():
    assert format_team_color("E10600") == "#E10600"
    assert format_team_color("#E10600") == "#E10600"
    assert format_team_color(None) == "#E10600"
