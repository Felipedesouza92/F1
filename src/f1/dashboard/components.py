"""Componentes de UI e renderizadores do Streamlit."""

from __future__ import annotations

import streamlit as st

from f1.domain.models import ClassificationEntry, WeatherSummary


def render_weather_metrics(weather: WeatherSummary | None) -> None:
    """Renderiza cartões com as métricas climáticas da sessão."""
    if not weather:
        st.info("Dados meteorológicos não disponíveis para esta sessão.")
        return

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "Temp. Ar",
            f"{weather.air_temp_last:.1f} °C" if weather.air_temp_last else "N/A",
            f"Min: {weather.air_temp_min or 0:.0f}° | Max: {weather.air_temp_max or 0:.0f}°",
        )
    with col2:
        st.metric(
            "Temp. Pista",
            f"{weather.track_temp_last:.1f} °C" if weather.track_temp_last else "N/A",
            f"Min: {weather.track_temp_min or 0:.0f}° | Max: {weather.track_temp_max or 0:.0f}°",
        )
    with col3:
        st.metric("Umidade", f"{weather.humidity_last or 0:.0f} %")
    with col4:
        st.metric("Chuva", "🌧️ Sim" if weather.rainfall else "☀️ Não")


def render_podium(classification: list[ClassificationEntry]) -> None:
    """Exibe cards especiais de destaque para o Top 3 da sessão."""
    top3 = classification[:3]
    if not top3:
        return

    cols = st.columns(3)
    order = [1, 0, 2] if len(top3) >= 3 else list(range(len(top3)))

    medals = {0: "🥇 1º Lugar", 1: "🥈 2º Lugar", 2: "🥉 3º Lugar"}

    for idx, pos in enumerate(order):
        if pos < len(top3):
            driver = top3[pos]
            with cols[idx]:
                st.markdown(
                    f"""
                    <div style="border-left: 6px solid {driver.team_colour};
                                background-color: #222222;
                                padding: 15px;
                                border-radius: 8px;
                                margin-bottom: 15px;">
                        <span style="font-size: 1.1em; color: #ffb703; font-weight: bold;">{medals.get(pos, "")}</span>
                        <h3 style="margin: 5px 0; color: #fafafa;">{driver.driver_name}</h3>
                        <p style="margin: 0; color: #aaaaaa;">{driver.team_name} | #{driver.driver_number}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
