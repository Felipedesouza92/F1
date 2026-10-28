"""Funções puras que geram gráficos Plotly para o dashboard."""

from __future__ import annotations

import plotly.graph_objects as go

from f1.domain.models import FastestLapEntry, StintBar
from f1.processing.formatting import COMPOUND_COLORS, format_lap_time

DARK_LAYOUT = dict(
    paper_bgcolor="#1a1a1a",
    plot_bgcolor="#222222",
    font=dict(color="#fafafa", family="sans-serif"),
    margin=dict(l=40, r=40, t=50, b=40),
)


def fastest_laps_bar(entries: list[FastestLapEntry]) -> go.Figure:
    """Gera gráfico de barras horizontais com as voltas mais rápidas."""
    fig = go.Figure()

    if not entries:
        fig.add_annotation(
            text="Nenhum dado de volta registrado para esta sessão.",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(color="#888888", size=16),
        )
        fig.update_layout(**DARK_LAYOUT, title="Voltas Mais Rápidas")
        return fig

    reversed_entries = list(reversed(entries))
    y_labels = [f"{e.driver_name} (#{e.driver_number})" for e in reversed_entries]
    x_values = [e.lap_duration for e in reversed_entries]
    colors = [e.team_colour for e in reversed_entries]
    text_labels = [format_lap_time(e.lap_duration) for e in reversed_entries]

    fig.add_trace(
        go.Bar(
            y=y_labels,
            x=x_values,
            orientation="h",
            marker=dict(color=colors),
            text=text_labels,
            textposition="auto",
            hovertemplate="<b>%{y}</b><br>Tempo: %{text}<extra></extra>",
        )
    )

    min_x = min(x_values) - 1.0
    max_x = max(x_values) + 1.0

    fig.update_layout(
        **DARK_LAYOUT,
        title="Top 10 Voltas Mais Rápidas",
        xaxis=dict(title="Duração (s)", range=[min_x, max_x], showgrid=True, gridcolor="#333333"),
        yaxis=dict(showgrid=False),
    )
    return fig


def pace_lines(driver_series: dict[int, list[tuple[int, float]]], driver_names: dict[int, str], driver_colors: dict[int, str]) -> go.Figure:
    """Gera gráfico de linha comparativo de ritmo volta a volta."""
    fig = go.Figure()

    has_data = False
    for num, points in driver_series.items():
        if not points:
            continue
        has_data = True
        laps = [p[0] for p in points]
        times = [p[1] for p in points]
        name = driver_names.get(num, f"#{num}")
        color = driver_colors.get(num, "#FFFFFF")

        fig.add_trace(
            go.Scatter(
                x=laps,
                y=times,
                mode="lines+markers",
                name=name,
                line=dict(color=color, width=2),
                marker=dict(size=4),
                hovertemplate=f"<b>{name}</b><br>Volta %{{x}}<br>Tempo: %{{y:.3f}}s<extra></extra>",
            )
        )

    if not has_data:
        fig.add_annotation(
            text="Selecione pilotos com voltas registradas para comparar o ritmo.",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(color="#888888", size=16),
        )

    fig.update_layout(
        **DARK_LAYOUT,
        title="Ritmo Volta a Volta (sem voltas de pit/outliers)",
        xaxis=dict(title="Número da Volta", showgrid=True, gridcolor="#333333"),
        yaxis=dict(title="Tempo de Volta (s)", showgrid=True, gridcolor="#333333"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def stint_timeline(stints: list[StintBar]) -> go.Figure:
    """Gera linha do tempo horizontal com compostos e duração dos stints."""
    fig = go.Figure()

    if not stints:
        fig.add_annotation(
            text="Nenhum dado de stint/pneus disponível para esta sessão.",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(color="#888888", size=16),
        )
        fig.update_layout(**DARK_LAYOUT, title="Estratégia de Pneus")
        return fig

    drivers_seen = sorted(list({s.driver_name for s in stints}), reverse=True)

    for compound, color in COMPOUND_COLORS.items():
        matching = [s for s in stints if s.compound == compound]
        if not matching:
            continue

        fig.add_trace(
            go.Bar(
                name=compound,
                y=[s.driver_name for s in matching],
                x=[(s.lap_end - s.lap_start + 1) for s in matching],
                base=[s.lap_start for s in matching],
                orientation="h",
                marker=dict(color=color, line=dict(color="#1a1a1a", width=1)),
                text=[f"{compound} ({s.lap_start}-{s.lap_end})" for s in matching],
                textposition="inside",
                insidetextanchor="middle",
                hovertemplate="<b>%{y}</b><br>Composto: " + compound + "<br>Voltas: %{base} a %{text}<extra></extra>",
            )
        )

    fig.update_layout(
        **DARK_LAYOUT,
        title="Estratégia de Pneus por Piloto",
        barmode="overlay",
        xaxis=dict(title="Volta", showgrid=True, gridcolor="#333333"),
        yaxis=dict(categoryorder="array", categoryarray=drivers_seen),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig

