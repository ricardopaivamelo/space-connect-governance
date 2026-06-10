"""Space Connect Governance — painel integrado de decisao.

Le data/integrated_snapshot.json (gerado por integration/build_snapshot.py)
e exibe modulos, metricas, alertas e a matriz de integracao. Decisoes humanas
sao persistidas em data/decision_log.jsonl.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from integration.decision_log import append_decision, build_decision_record, read_decisions

REPO_ROOT = Path(__file__).resolve().parent
SNAPSHOT_PATH = REPO_ROOT / "data" / "integrated_snapshot.json"
NEURO_SERIES_PATH = REPO_ROOT / "integration" / "sources" / "neuromorphic_saida_ajuste_b.csv"

SEVERITY_COLORS = {"CRÍTICO": "#d62728", "CRITICO": "#d62728", "ALERTA": "#ff7f0e", "NOMINAL": "#2ca02c"}
LEVEL_LABELS = {
    "integrated_data_source": "Integrado (fonte de dados)",
    "integrated_ui": "Integrado (interface)",
    "evidence_only": "Evidencia auditada",
    "conceptual": "Conceitual",
    "not_integrated": "Nao integrado",
}


@st.cache_data(show_spinner=False)
def load_snapshot() -> dict:
    return json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))


@st.cache_data(show_spinner=False)
def load_neuro_series() -> pd.DataFrame:
    return pd.read_csv(NEURO_SERIES_PATH)


def render_overview(snapshot: dict) -> None:
    metrics = snapshot["metrics"]
    cols = st.columns(4)
    cols[0].metric("Modulos no ecossistema", metrics["modules_total"])
    cols[1].metric("Tecnicamente integrados", metrics["modules_integrated"])
    cols[2].metric("Alertas consolidados", metrics["alerts_total"])
    cols[3].metric("Falhas tratadas pelo RPA", metrics["rpa_failures_handled"])
    st.caption(f"Snapshot gerado em {snapshot['generated_at']} (UTC). Cenario: {snapshot['scenario']}")

    rows = [
        {
            "Modulo": m["name"],
            "Disciplina": m["discipline"],
            "Integracao": LEVEL_LABELS.get(m["integration_level"], m["integration_level"]),
            "Origem dos dados": m["data_origin"],
            "Verificacao": m["verification_level"],
        }
        for m in snapshot["modules"]
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def render_modules(snapshot: dict) -> None:
    for module in snapshot["modules"]:
        label = LEVEL_LABELS.get(module["integration_level"], module["integration_level"])
        with st.expander(f"{module['name']} — {module['discipline']} [{label}]"):
            st.write(f"**Status:** {module['status']}")
            st.write(f"**Origem dos dados:** `{module['data_origin']}` | **Verificacao:** `{module['verification_level']}`")
            if module["metrics"]:
                st.json(module["metrics"])
            if module["limitations"]:
                st.markdown("**Limitacoes declaradas:**")
                for limitation in module["limitations"]:
                    st.markdown(f"- {limitation}")
            if module["evidence"]:
                st.caption("Evidencias: " + ", ".join(module["evidence"]))


def render_neuro_chart() -> None:
    if not NEURO_SERIES_PATH.exists():
        st.info("Serie do sensor neuromorfico nao encontrada.")
        return
    df = load_neuro_series()
    fig = px.line(df, x="tempo_min", y="estado_memristor", title="Sensor neuromorfico — Ajuste B (reexecucao da entrega)")
    fig.add_scatter(
        x=df["tempo_min"], y=df["estado_memristor"], mode="markers", name="LED",
        marker={"color": df["LED"].map({"APAGADO": "#2ca02c", "AMARELO": "#ff7f0e", "VERMELHO": "#d62728"})},
    )
    fig.add_hline(y=0.35, line_dash="dot", annotation_text="limiar OBSERVACAO (0,35)")
    fig.add_hline(y=0.70, line_dash="dot", annotation_text="limiar ALERTA_CRITICO (0,70)")
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Reexecucao local do notebook entregue com o dataset oficial de 61 leituras. "
        "Limitacao declarada: a dinamica nao usa delta_t e depende da frequencia de amostragem."
    )


def render_decisions(snapshot: dict) -> None:
    alerts = snapshot["alerts"]
    st.subheader("Alertas que exigem decisao humana")
    table = pd.DataFrame(
        [{"ID": a["alert_id"], "Origem": a["source_module"], "Severidade": a["severity"], "Titulo": a["title"]} for a in alerts]
    )
    st.dataframe(table, use_container_width=True, hide_index=True)

    options = {f"[{a['severity']}] {a['title']}": a for a in alerts}
    selected_label = st.selectbox("Alerta em analise", list(options.keys()))
    selected = options[selected_label]
    st.info(selected["detail"])

    operator = st.text_input("Operador responsavel")
    justification = st.text_area("Justificativa da decisao")
    ready = bool(operator.strip()) and bool(justification.strip())
    if not ready:
        st.caption("Preencha operador e justificativa para habilitar a decisao (exigencia de governanca).")

    col_a, col_b = st.columns(2)
    decision = None
    if col_a.button("Aprovar acao do alerta", type="primary", disabled=not ready):
        decision = "APROVADO"
    if col_b.button("Rejeitar alerta", disabled=not ready):
        decision = "REJEITADO"
    if decision:
        record = build_decision_record(
            alert_id=selected["alert_id"],
            decision=decision,
            operator=operator,
            justification=justification,
            source_module=selected["source_module"],
            snapshot_generated_at=snapshot["generated_at"],
        )
        append_decision(record)
        st.success(f"Decisao {decision} registrada em data/decision_log.jsonl")

    st.subheader("Trilha de auditoria (persistida em disco)")
    decisions = read_decisions()
    if decisions:
        st.dataframe(pd.DataFrame(decisions), use_container_width=True, hide_index=True)
    else:
        st.caption("Nenhuma decisao registrada ate o momento.")


def render_governance(snapshot: dict) -> None:
    st.subheader("Matriz de integracao")
    st.dataframe(pd.DataFrame(snapshot["integration_matrix"]), use_container_width=True, hide_index=True)
    st.subheader("Controles de governanca")
    for key, value in snapshot["governance"].items():
        st.markdown(f"- **{key}**: {value}")
    st.subheader("Limitacoes globais declaradas")
    for limitation in snapshot["limitations"]:
        st.markdown(f"- {limitation}")
    st.caption("Artefatos-fonte: " + ", ".join(snapshot["source_artifacts"]))


def main() -> None:
    st.set_page_config(page_title="Space Connect Governance", page_icon="🛰️", layout="wide")
    if not SNAPSHOT_PATH.exists():
        st.error("Snapshot nao encontrado. Execute: python integration/build_snapshot.py")
        st.stop()
    snapshot = load_snapshot()
    st.title("Space Connect Governance — painel integrado")
    st.caption("Integracao minima real: artefatos verificados -> snapshot JSON -> painel -> decisao humana auditavel.")

    tab_overview, tab_modules, tab_neuro, tab_decision, tab_gov = st.tabs(
        ["Panorama", "Modulos", "Sensor neuromorfico", "Decisao humana", "Governanca"]
    )
    with tab_overview:
        render_overview(snapshot)
    with tab_modules:
        render_modules(snapshot)
    with tab_neuro:
        render_neuro_chart()
    with tab_decision:
        render_decisions(snapshot)
    with tab_gov:
        render_governance(snapshot)


main()
