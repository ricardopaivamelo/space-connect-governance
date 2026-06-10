"""
dashboard.py
============
Front-end (Streamlit) que carrega os dados estruturados gerados pelo robô
(outputs/resultado.json) e exibe um painel de controle da missão.

Como usar:
    1. Rode o robô primeiro:   python run.py
    2. Suba o dashboard:       streamlit run dashboard.py

Demonstra o critério "carga de dados estruturados para o front-end".
"""

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from robo.config import Config

st.set_page_config(page_title="MissionOps RPA — Painel", page_icon="🛰️",
                   layout="wide")

cfg = Config()
caminho_json = cfg.pasta_outputs / cfg.arq_json

st.title("🛰️ MissionOps RPA — Painel de Triagem de Missão")

if not caminho_json.exists():
    st.warning(
        "Nenhum resultado encontrado. Rode o robô primeiro com `python run.py` "
        "para gerar os dados, depois recarregue esta página."
    )
    st.stop()

dados = json.loads(caminho_json.read_text(encoding="utf-8"))
est = dados["estatisticas"]
res = dados["resultados"]

st.caption(f"Última execução processada em {dados['gerado_em']}")

# ---- Indicadores ----
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Processados", est["total_processados"])
c2.metric("Falhas tratadas", est["total_falhas"])
c3.metric("Telemetrias críticas", est["telemetria_criticas"])
c4.metric("Docs crít./alerta", est["documentos_criticos"])
c5.metric("Imagens anômalas", est["imagens_anomalas"])

st.divider()

# ---- Abas por tipo de dado ----
aba_tel, aba_doc, aba_img, aba_falhas = st.tabs(
    ["📊 Telemetria", "📄 Documentos", "🛰️ Imagens", "⚠️ Falhas"]
)


def _cor_severidade(val):
    cores = {"CRÍTICO": "#FFCDD2", "ANOMALIA": "#FFCDD2",
             "ALERTA": "#FFE0B2", "NOMINAL": "#C8E6C9"}
    return f"background-color: {cores.get(val, '')}"


with aba_tel:
    if res["telemetria"]:
        df = pd.DataFrame([{
            "Arquivo": r["nome"], "Linhas": r["linhas"],
            "Outliers (z-score)": r["n_anomalias_zscore"],
            "Flags ML (IsolationForest)": r["n_anomalias_isolationforest"],
            "Severidade": r["severidade"],
        } for r in res["telemetria"]])
        st.dataframe(df.style.applymap(_cor_severidade, subset=["Severidade"]),
                     use_container_width=True)
    else:
        st.info("Sem telemetrias processadas.")

with aba_doc:
    if res["documentos"]:
        df = pd.DataFrame([{
            "Arquivo": r["nome"], "Palavras": r["palavras"],
            "Severidade": r["severidade"],
            "Códigos de erro": ", ".join(r["entidades"]["codigos_erro"]) or "-",
            "Subsistemas": ", ".join(r["entidades"]["subsistemas"]) or "-",
        } for r in res["documentos"]])
        st.dataframe(df.style.applymap(_cor_severidade, subset=["Severidade"]),
                     use_container_width=True)
    else:
        st.info("Sem documentos processados.")

with aba_img:
    if res["imagens"]:
        df = pd.DataFrame([{
            "Arquivo": r["nome"], "Dimensões": f"{r['largura']}x{r['altura']}",
            "Brilho médio": r["brilho_medio"], "% Hotspots": r["perc_hotspots"],
            "Severidade": r["severidade"],
        } for r in res["imagens"]])
        st.dataframe(df.style.applymap(_cor_severidade, subset=["Severidade"]),
                     use_container_width=True)
    else:
        st.info("Sem imagens processadas.")

with aba_falhas:
    if est["falhas"]:
        st.error(f"{len(est['falhas'])} arquivo(s) falharam (tratados pelo robô):")
        st.dataframe(pd.DataFrame(est["falhas"]), use_container_width=True)
    else:
        st.success("Nenhuma falha de processamento nesta execução.")

st.divider()
st.caption("Artefatos completos em outputs/: relatorio_missao.xlsx e "
           "relatorio_missao.pdf")
