"""Funções de processamento de classificação e resultados da sessão."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from f1.domain.models import ClassificationEntry, Driver


def build_classification(
    drivers: list[Driver], driver_index: dict[int, Driver]
) -> list[ClassificationEntry]:
    """Constrói a lista de classificação a partir dos pilotos disponíveis."""
    from f1.domain.models import ClassificationEntry

    entries: list[ClassificationEntry] = []
    for idx, driver in enumerate(drivers, start=1):
        color = driver.team_colour or "FFFFFF"
        if not color.startswith("#"):
            color = f"#{color}"

        entries.append(
            ClassificationEntry(
                position=idx,
                driver_number=driver.driver_number,
                driver_name=driver.full_name or f"Piloto {driver.driver_number}",
                team_name=driver.team_name or "Desconhecida",
                team_colour=color,
                status="Finished",
            )
        )
    return entries

