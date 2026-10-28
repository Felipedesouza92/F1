"""Testes unitários para os modelos Pydantic de f1/domain/models.py."""

import pytest
from pydantic import ValidationError

from f1.domain.models import Driver, Lap, Meeting, Session, Stint


def test_meeting_model():
    m = Meeting(
        meeting_key=1234,
        meeting_name="Monaco Grand Prix",
        year=2024,
        country_name="Monaco",
        circuit_short_name="Monaco",
    )
    assert m.meeting_key == 1234
    assert m.meeting_name == "Monaco Grand Prix"


def test_driver_model_extra_fields_ignored():
    d = Driver(
        driver_number=1,
        full_name="Max Verstappen",
        team_name="Red Bull Racing",
        extra_unknown_field="should_be_ignored",
    )
    assert d.driver_number == 1
    assert d.full_name == "Max Verstappen"
    assert not hasattr(d, "extra_unknown_field")


def test_lap_model():
    lap = Lap(
        driver_number=44,
        lap_number=12,
        lap_duration=83.456,
        duration_sector_1=25.1,
        duration_sector_2=30.2,
        duration_sector_3=28.156,
    )
    assert lap.lap_duration == 83.456
    assert lap.is_pit_out_lap is False


def test_stint_model_validation():
    s = Stint(
        driver_number=16,
        stint_number=1,
        compound="SOFT",
        lap_start=1,
        lap_end=18,
    )
    assert s.compound == "SOFT"

