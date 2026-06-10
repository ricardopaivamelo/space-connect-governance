from __future__ import annotations
import time
import streamlit as st
from providers.climate_provider import load_mock_satellite_data, REGIONS, CATEGORIES
from pipelines.risk_pipeline import calculate_risk_score, filter_data, summarize_metrics, recommended_action
from state.session_state import register_decision
from ui.components import metric_card, plot_risk_timeline, plot_category_bar, plot_population_matplotlib, risk_badge


@st.cache_data(show_spinner=False)
def get_data():
    time.sleep(0.7)  # simula latência de API/satélite para demonstrar design de latência
    raw = load_mock_satellite_data()
    return calculate_risk_score(raw)


def render_sidebar(df):
    st.sidebar.header("Filtros de decisão")
    min_date = df["data"].min().date()
    max_date = df["data"].max().date()
    date_range = st.sidebar.date_input("Intervalo de datas", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    if len(date_range) != 2:
        date_range = (min_date, max_date)
    regions = st.sidebar.multiselect("Região geográfica", REGIONS, default=REGIONS)
    categories = st.sidebar.multiselect("Categoria do evento", CATEGORIES, default=CATEGORIES)
    min_risk = st.sidebar.slider("Threshold mínimo de risco", 0, 160, 35, 5)
    return date_range[0], date_range[1], regions, categories, float(min_risk)


def render_dashboard():
    st.title("GeoGuard IA — Dashboard de Risco Climático e Satelital")
    st.caption("POC para transformar dados climáticos/satelitais em decisão operacional para gestores não-técnicos.")

    with st.spinner("Carregando e enriquecendo dados satelitais simulados..."):
        progress = st.progress(0)
        for step in range(0, 101, 25):
            progress.progress(step)
            time.sleep(0.05)
        df = get_data()
        progress.empty()

    start_date, end_date, regions, categories, min_risk = render_sidebar(df)
    filtered = filter_data(df, start_date, end_date, regions, categories, min_risk)
    metrics = summarize_metrics(filtered)

    tab_overview, tab_detail, tab_decision = st.tabs(["Panorama", "Análise", "Decisão humana"])

    with tab_overview:
        cols = st.columns(4)
        with cols[0]: metric_card("Risco médio", metrics["risco_medio"], "Média do score no recorte filtrado")
        with cols[1]: metric_card("Alertas críticos", metrics["alertas_criticos"])
        with cols[2]: metric_card("População exposta", f"{metrics['populacao_exposta']:,}".replace(",", "."))
        with cols[3]: metric_card("Focos de calor", metrics["focos_calor"])
        if filtered.empty:
            st.warning("Nenhum dado encontrado para os filtros selecionados.")
        else:
            top_level = filtered.sort_values("risco_score", ascending=False).iloc[0]["nivel_risco"]
            st.markdown(f"**Maior criticidade no recorte:** {risk_badge(top_level)}", unsafe_allow_html=True)
            st.plotly_chart(plot_risk_timeline(filtered), use_container_width=True)

    with tab_detail:
        col1, col2 = st.columns([1, 1])
        with col1:
            if not filtered.empty:
                st.plotly_chart(plot_category_bar(filtered), use_container_width=True)
        with col2:
            if not filtered.empty:
                st.pyplot(plot_population_matplotlib(filtered))
        st.dataframe(filtered.sort_values("risco_score", ascending=False).head(30), use_container_width=True)

    with tab_decision:
        action = recommended_action(filtered)
        st.subheader("Insight gerado pelo sistema")
        st.info(action)
        st.write("O operador precisa validar a recomendação antes de qualquer alerta operacional.")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Aprovar envio do alerta", type="primary"):
                register_decision(action, True)
                st.success("Decisão aprovada e registrada no estado da sessão.")
        with col_b:
            if st.button("Rejeitar alerta"):
                register_decision(action, False)
                st.error("Decisão rejeitada e registrada no estado da sessão.")
        st.markdown(f"**Última decisão:** {st.session_state.last_decision}")
        st.write("Histórico da sessão:")
        st.write(st.session_state.approved_alerts)
