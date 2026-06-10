"""
processadores/telemetria.py
===========================
IA aplicada à telemetria de missão (arquivos CSV).

Combina dois algoritmos de análise para detectar leituras anômalas:
  1. Z-score por variável (detecção estatística univariada).
  2. Isolation Forest (modelo de ML não supervisionado, multivariado).

Saída: resumo por arquivo com nº de leituras, nº de anomalias, colunas
monitoradas e os instantes/linhas mais críticos.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from ..config import Config


def processar_telemetria(caminho: Path, cfg: Config) -> Dict:
    """Processa um CSV de telemetria e devolve um dicionário com o resultado."""
    df = pd.read_csv(caminho)

    if df.empty:
        raise ValueError("CSV de telemetria sem linhas.")

    # Seleciona apenas colunas numéricas para a análise
    colunas_num = df.select_dtypes(include=[np.number]).columns.tolist()
    if not colunas_num:
        raise ValueError("Nenhuma coluna numérica encontrada na telemetria.")

    dados = df[colunas_num].fillna(df[colunas_num].mean())

    # --- 1) Z-score univariado ---
    media = dados.mean()
    desvio = dados.std(ddof=0).replace(0, np.nan)
    z = (dados - media) / desvio
    z_max_por_linha = z.abs().max(axis=1).fillna(0)
    anomalia_z = z_max_por_linha > cfg.z_score_limite

    # --- 2) Isolation Forest multivariado ---
    # contamination define a fração esperada de anomalias
    modelo = IsolationForest(
        contamination=cfg.contaminacao_isolation_forest,
        random_state=42,
        n_estimators=120,
    )
    pred = modelo.fit_predict(dados)        # -1 = anomalia, 1 = normal
    score = -modelo.score_samples(dados)    # maior = mais anômalo
    anomalia_if = pred == -1

    # Anomalia (para contagem/contexto) = qualquer um dos métodos sinaliza
    anomalia = anomalia_z | anomalia_if
    n_anomalias = int(anomalia.sum())
    n_anomalias_z = int(anomalia_z.sum())
    n_anomalias_if = int(anomalia_if.sum())

    # Top linhas mais críticas (maior score do Isolation Forest)
    idx_top = np.argsort(score)[::-1][:5]
    criticos = []
    for i in idx_top:
        if anomalia.iloc[i]:
            criticos.append({
                "linha": int(i),
                "score_anomalia": round(float(score[i]), 4),
                "z_max": round(float(z_max_por_linha.iloc[i]), 2),
            })

    # Severidade baseada em outliers estatísticos REAIS (|z| > limiar):
    # evita falso positivo em dados nominais. O Isolation Forest entra como
    # contexto multivariado e ranqueamento das linhas mais suspeitas.
    severidade = "CRÍTICO" if n_anomalias_z > 0 else "NOMINAL"

    return {
        "nome": caminho.name,
        "tipo": "telemetria",
        "linhas": int(len(df)),
        "colunas_monitoradas": colunas_num,
        "n_anomalias": n_anomalias,
        "n_anomalias_zscore": n_anomalias_z,
        "n_anomalias_isolationforest": n_anomalias_if,
        "perc_anomalias": round(100 * n_anomalias / len(df), 2),
        "severidade": severidade,
        "leituras_criticas": criticos,
        "resumo": (
            f"{len(df)} leituras; {n_anomalias_z} outlier(s) confirmado(s) "
            f"(z-score) e {n_anomalias_if} flag(s) do Isolation Forest, "
            f"em {len(colunas_num)} variáveis."
        ),
    }
