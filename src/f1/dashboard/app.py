"""Ponto de entrada (composition root) da aplicação Streamlit."""

from __future__ import annotations

import streamlit as st

from f1.dashboard.charts import fastest_laps_bar, pace_lines, stint_timeline
from f1.dashboard.components import render_podium, render_weather_metrics
from f1.domain.services import F1DashboardService
from f1.ingestion.http_client import HttpClient, OpenF1ApiError
from f1.ingestion.openf1_repositories import (
    OpenF1DriverRepository,
    OpenF1LapRepository,
    OpenF1MeetingRepository,
    OpenF1PitRepository,
    OpenF1SessionRepository,
    OpenF1StintRepository,
    OpenF1WeatherRepository,
)
from f1.processing.formatting import format_lap_time
from f1.processing.laps import lap_time_series
from f1.utils.config import load_settings
from f1.utils.logger import configurar_logging, get_logger

st.set_page_config(
    page_title="F1 Dashboard",
    page_icon="🏎️",
    layout="wide",
)

logger = get_logger(__name__)


@st.cache_resource
def get_service() -> F1DashboardService:
    """Instancia clientes e repositórios uma única vez."""
    settings = load_settings()
    configurar_logging(settings.log_level)
    client = HttpClient(base_url=settings.base_url, timeout=settings.timeout)

    return F1DashboardService(
        meetings=OpenF1MeetingRepository(client),
        sessions=OpenF1SessionRepository(client),
        drivers=OpenF1DriverRepository(client),
        laps=OpenF1LapRepository(client),
        stints=OpenF1StintRepository(client),
        pits=OpenF1PitRepository(client),
        weather=OpenF1WeatherRepository(client),
    )


def main() -> None:
    """Função principal que renderiza a aplicação."""
    service = get_service()

    st.sidebar.title("🏎️ F1 OpenF1 Dashboard")
    year = st.sidebar.selectbox("Temporada", options=[2024, 2023], index=0)

    try:
        meetings = service.list_meetings(year)
    except OpenF1ApiError as e:
        logger.error("Erro ao listar GPs: %s", e)
        st.error(f"Não foi possível conectar à OpenF1 API: {e}")
        return

    if not meetings:
        st.warning(f"Nenhum GP encontrado para o ano {year}.")
        return

    meeting_map = {
        f"{m.meeting_name} ({m.circuit_short_name or ''})": m for m in meetings
    }
    selected_meeting_name = st.sidebar.selectbox(
        "Grande Prêmio", list(meeting_map.keys())
    )
    selected_meeting = meeting_map[selected_meeting_name]

    sessions = service.list_sessions(selected_meeting.meeting_key)
    if not sessions:
        st.warning("Nenhuma sessão encontrada para este GP.")
        return

    session_map = {f"{s.session_name} ({s.session_type or ''})": s for s in sessions}
    selected_session_name = st.sidebar.selectbox("Sessão", list(session_map.keys()))
    selected_session = session_map[selected_session_name]

    st.sidebar.markdown("---")
    st.sidebar.caption(
        "Dados fornecidos gratuitamente por [OpenF1](https://openf1.org)."
    )

    # Cabeçalho Principal
    st.title(f"🏁 {selected_meeting.meeting_name} — {selected_session.session_name}")
    st.caption(
        f"Circuito: {selected_meeting.circuit_short_name} | Ano: {selected_meeting.year}"
    )

    with st.spinner("Carregando telemetria e dados da sessão..."):
        try:
            overview = service.get_session_overview(selected_session.session_key)
        except OpenF1ApiError as e:
            logger.error("Erro ao carregar sessão: %s", e)
            st.error(f"Erro ao processar dados da sessão: {e}")
            return

    # Clima
    render_weather_metrics(overview.weather)
    st.markdown("---")

    tab_res, tab_laps, tab_pace, tab_stints = st.tabs(
        [
            "🏆 Resultado",
            "⚡ Melhores Voltas",
            "📈 Ritmo de Corrida",
            "🛞 Estratégia de Pneus",
        ]
    )

    with tab_res:
        if overview.classification:
            render_podium(overview.classification)
            st.subheader("Classificação Geral")
            table_data = [
                {
                    "Pos": c.position,
                    "Piloto": c.driver_name,
                    "Nº": c.driver_number,
                    "Equipe": c.team_name,
                    "Status": c.status,
                }
                for c in overview.classification
            ]
            st.dataframe(table_data, use_container_width=True)
        else:
            st.info("Nenhum dado de classificação disponível para esta sessão.")

    with tab_laps:
        st.plotly_chart(
            fastest_laps_bar(overview.fastest_laps), use_container_width=True
        )
        if overview.fastest_laps:
            laps_table = [
                {
                    "Piloto": e.driver_name,
                    "Nº": e.driver_number,
                    "Equipe": e.team_name,
                    "Melhor Volta": format_lap_time(e.lap_duration),
                    "Setor 1": f"{e.sector_1:.3f}s" if e.sector_1 else "-",
                    "Setor 2": f"{e.sector_2:.3f}s" if e.sector_2 else "-",
                    "Setor 3": f"{e.sector_3:.3f}s" if e.sector_3 else "-",
                }
                for e in overview.fastest_laps
            ]
            st.dataframe(laps_table, use_container_width=True)

    with tab_pace:
        if overview.drivers:
            driver_choices = {
                f"{d.full_name} (#{d.driver_number})": d.driver_number
                for d in overview.drivers
            }
            default_selection = list(driver_choices.keys())[:3]
            selected_names = st.multiselect(
                "Selecione pilotos para comparar ritmo:",
                options=list(driver_choices.keys()),
                default=default_selection,
            )
            selected_numbers = [driver_choices[name] for name in selected_names]

            raw_laps = service._laps.list(selected_session.session_key)
            series = lap_time_series(raw_laps, selected_numbers)

            names_map = {
                d.driver_number: d.full_name or f"#{d.driver_number}"
                for d in overview.drivers
            }
            colors_map = {
                d.driver_number: f"#{d.team_colour or 'FFFFFF'}"
                for d in overview.drivers
            }

            st.plotly_chart(
                pace_lines(series, names_map, colors_map), use_container_width=True
            )
        else:
            st.info("Sem dados de telemetria disponíveis.")

    with tab_stints:
        st.plotly_chart(
            stint_timeline(overview.stint_timeline), use_container_width=True
        )
        if overview.pit_stops:
            st.subheader("Paradas nos Boxes (Pit Stops)")
            pit_table = [
                {
                    "Piloto": p.driver_name,
                    "Nº": p.driver_number,
                    "Volta": p.lap_number,
                    "Duração (s)": f"{p.pit_duration:.2f}s"
                    if p.pit_duration
                    else "N/A",
                }
                for p in overview.pit_stops
            ]
            st.dataframe(pit_table, use_container_width=True)


if __name__ == "__main__":
    main()
