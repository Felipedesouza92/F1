"""Funções de processamento e formatação de voltas (puras, sem I/O)."""

from __future__ import annotations

import statistics
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from f1.domain.models import Driver, FastestLapEntry, Lap


def build_driver_index(drivers: list[Driver]) -> dict[int, Driver]:
    """Cria um dicionário indexado pelo driver_number."""
    return {d.driver_number: d for d in drivers}


def filter_valid_laps(laps: list[Lap]) -> list[Lap]:
    """Filtra apenas voltas válidas (com duração definida e não sendo volta de saída do pit)."""
    return [
        lap
        for lap in laps
        if lap.lap_duration is not None
        and lap.lap_duration > 0
        and not lap.is_pit_out_lap
    ]


def compute_top_n_laps(
    laps: list[Lap], driver_index: dict[int, Driver], n: int = 10
) -> list[FastestLapEntry]:
    """Calcula a melhor volta por piloto e retorna as Top N ordenadas."""
    from f1.domain.models import FastestLapEntry

    valid = filter_valid_laps(laps)
    best_per_driver: dict[int, Lap] = {}

    for lap in valid:
        assert lap.lap_duration is not None
        num = lap.driver_number
        if num not in best_per_driver:
            best_per_driver[num] = lap
        else:
            current_best = best_per_driver[num].lap_duration
            if current_best is not None and lap.lap_duration < current_best:
                best_per_driver[num] = lap

    sorted_laps = sorted(
        best_per_driver.values(),
        key=lambda l: l.lap_duration if l.lap_duration is not None else float("inf"),
    )[:n]

    results: list[FastestLapEntry] = []
    for lap in sorted_laps:
        assert lap.lap_duration is not None
        driver = driver_index.get(lap.driver_number)
        name = driver.full_name if driver and driver.full_name else f"#{lap.driver_number}"
        team = driver.team_name if driver and driver.team_name else "Independente"
        color = driver.team_colour if driver and driver.team_colour else "FFFFFF"
        if not color.startswith("#"):
            color = f"#{color}"

        results.append(
            FastestLapEntry(
                driver_number=lap.driver_number,
                driver_name=name,
                team_name=team,
                team_colour=color,
                lap_duration=lap.lap_duration,
                sector_1=lap.duration_sector_1,
                sector_2=lap.duration_sector_2,
                sector_3=lap.duration_sector_3,
            )
        )

    return results


def lap_time_series(
    laps: list[Lap], driver_numbers: list[int]
) -> dict[int, list[tuple[int, float]]]:
    """Retorna a série temporal de ritmo de voltas (lap_number, lap_duration) sem outliers (>107% da mediana)."""
    valid = filter_valid_laps(laps)
    by_driver: dict[int, list[Lap]] = {num: [] for num in driver_numbers}

    for lap in valid:
        if lap.driver_number in by_driver and lap.lap_duration is not None:
            by_driver[lap.driver_number].append(lap)

    series: dict[int, list[tuple[int, float]]] = {}
    for num, driver_laps in by_driver.items():
        if not driver_laps:
            series[num] = []
            continue

        durations = [l.lap_duration for l in driver_laps if l.lap_duration is not None]
        if not durations:
            series[num] = []
            continue

        med = statistics.median(durations)
        cutoff = med * 1.07

        filtered = [
            (l.lap_number, l.lap_duration)
            for l in driver_laps
            if l.lap_duration is not None and l.lap_duration <= cutoff
        ]
        series[num] = sorted(filtered, key=lambda x: x[0])

    return series

