"""Funções de processamento de stints e paradas nos boxes."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from f1.domain.models import Driver, PitStop, PitSummary, Stint, StintBar


def build_stint_timeline(
    stints: list[Stint], driver_index: dict[int, Driver]
) -> list[StintBar]:
    """Processa stints para projeção na linha do tempo horizontal."""
    from f1.domain.models import StintBar

    timeline: list[StintBar] = []
    for s in stints:
        if s.lap_start is None or s.lap_end is None:
            continue
        driver = driver_index.get(s.driver_number)
        name = driver.full_name if driver and driver.full_name else f"#{s.driver_number}"
        compound = (s.compound or "UNKNOWN").upper()

        timeline.append(
            StintBar(
                driver_number=s.driver_number,
                driver_name=name,
                compound=compound,
                lap_start=s.lap_start,
                lap_end=s.lap_end,
            )
        )
    return sorted(timeline, key=lambda x: (x.driver_name, x.lap_start))


def pit_summary(
    pits: list[PitStop], driver_index: dict[int, Driver]
) -> list[PitSummary]:
    """Gera resumo dos pit stops para exibição tabular."""
    from f1.domain.models import PitSummary

    summary: list[PitSummary] = []
    for p in pits:
        driver = driver_index.get(p.driver_number)
        name = driver.full_name if driver and driver.full_name else f"#{p.driver_number}"
        summary.append(
            PitSummary(
                driver_number=p.driver_number,
                driver_name=name,
                lap_number=p.lap_number,
                pit_duration=p.pit_duration,
            )
        )
    return sorted(summary, key=lambda x: (x.lap_number or 0, x.driver_name))

