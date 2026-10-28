"""Funções utilitárias de formatação para exibição."""

COMPOUND_COLORS: dict[str, str] = {
    "SOFT": "#FF3333",
    "MEDIUM": "#FFF200",
    "HARD": "#FFFFFF",
    "INTERMEDIATE": "#39B54A",
    "WET": "#00AEEF",
    "UNKNOWN": "#888888",
}


def format_lap_time(seconds: float | None) -> str:
    """Converte segundos em formato de volta F1 (ex: 83.456 -> '1:23.456')."""
    if seconds is None or seconds <= 0:
        return "--:--.---"
    minutes = int(seconds // 60)
    rem_seconds = seconds % 60
    return f"{minutes}:{rem_seconds:06.3f}"


def format_team_color(color_hex: str | None, default: str = "#E10600") -> str:
    """Garante formato hex válido com #."""
    if not color_hex:
        return default
    return color_hex if color_hex.startswith("#") else f"#{color_hex}"
