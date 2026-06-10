from __future__ import annotations
import pandas as pd


def calculate_risk_score(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["risco_score"] = (
        data["focos_calor"] * 2.2
        + data["indice_seca"] * 1.3
        + data["indice_enchente"] * 1.1
        + (100 - data["umidade_pct"]) * 0.25
        + data["vento_kmh"] * 0.4
    ).round(1)
    data["nivel_risco"] = pd.cut(
        data["risco_score"],
        bins=[-1, 35, 70, 110, 10_000],
        labels=["Baixo", "Moderado", "Alto", "Crítico"],
    ).astype(str)
    return data


def filter_data(df: pd.DataFrame, start_date, end_date, regions: list[str], categories: list[str], min_risk: float) -> pd.DataFrame:
    data = df.copy()
    data["data"] = pd.to_datetime(data["data"])
    mask = (
        (data["data"].dt.date >= start_date)
        & (data["data"].dt.date <= end_date)
        & (data["regiao"].isin(regions))
        & (data["categoria"].isin(categories))
        & (data["risco_score"] >= min_risk)
    )
    return data.loc[mask].sort_values("data")


def summarize_metrics(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"risco_medio": 0, "alertas_criticos": 0, "populacao_exposta": 0, "focos_calor": 0}
    return {
        "risco_medio": round(float(df["risco_score"].mean()), 1),
        "alertas_criticos": int((df["nivel_risco"] == "Crítico").sum()),
        "populacao_exposta": int(df.loc[df["nivel_risco"].isin(["Alto", "Crítico"]), "populacao_exposta"].sum()),
        "focos_calor": int(df["focos_calor"].sum()),
    }


def recommended_action(df: pd.DataFrame) -> str:
    if df.empty:
        return "Nenhum alerta necessário no recorte atual."
    critical = df[df["nivel_risco"] == "Crítico"]
    if not critical.empty:
        top_region = critical.groupby("regiao")["risco_score"].mean().idxmax()
        return f"Enviar alerta preventivo para {top_region}: risco crítico detectado no recorte filtrado."
    high = df[df["nivel_risco"] == "Alto"]
    if not high.empty:
        top_region = high.groupby("regiao")["risco_score"].mean().idxmax()
        return f"Monitorar {top_region} e preparar equipes locais: risco alto em evolução."
    return "Manter monitoramento de rotina. Não há risco alto ou crítico no filtro atual."
