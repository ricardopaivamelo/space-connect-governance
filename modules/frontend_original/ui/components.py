from __future__ import annotations
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

RISK_COLORS = {"Baixo": "#2E7D32", "Moderado": "#F9A825", "Alto": "#EF6C00", "Crítico": "#C62828"}


def risk_badge(level: str) -> str:
    color = RISK_COLORS.get(level, "#607D8B")
    return f"<span style='background:{color};color:white;padding:6px 10px;border-radius:999px;font-weight:700'>{level}</span>"


def metric_card(label: str, value, help_text: str = "") -> None:
    st.metric(label, value, help=help_text)


def plot_risk_timeline(df: pd.DataFrame):
    daily = df.groupby(["data", "regiao"], as_index=False)["risco_score"].mean()
    fig = px.line(daily, x="data", y="risco_score", color="regiao", markers=True, title="Evolução do risco por região")
    fig.update_layout(hovermode="x unified", yaxis_title="Score de risco", xaxis_title="Data")
    return fig


def plot_category_bar(df: pd.DataFrame):
    grouped = df.groupby(["categoria", "nivel_risco"], as_index=False).size()
    fig = px.bar(grouped, x="categoria", y="size", color="nivel_risco", title="Ocorrências por categoria e nível", color_discrete_map=RISK_COLORS)
    fig.update_layout(yaxis_title="Ocorrências", xaxis_title="Categoria")
    return fig


def plot_population_matplotlib(df: pd.DataFrame):
    grouped = df.groupby("regiao")["populacao_exposta"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    grouped.plot(kind="bar", ax=ax)
    ax.set_title("População exposta por região")
    ax.set_xlabel("Região")
    ax.set_ylabel("Pessoas expostas")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    return fig
