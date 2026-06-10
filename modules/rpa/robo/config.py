"""
config.py
=========
Configurações centrais do robô MissionOps RPA.
Centraliza caminhos, parâmetros dos modelos e limiares de anomalia,
para que nenhum valor fique "espalhado" pelo código.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

# Raiz do projeto (pasta que contém este arquivo -> sobe um nível)
RAIZ = Path(__file__).resolve().parent.parent


@dataclass
class Config:
    # --- Pastas do fluxo ---
    pasta_inbox: Path = RAIZ / "inbox"
    pasta_outputs: Path = RAIZ / "outputs"
    pasta_logs: Path = RAIZ / "logs"

    # --- Extensões reconhecidas por tipo de dado ---
    ext_telemetria: tuple = (".csv",)
    ext_documentos: tuple = (".txt", ".log", ".pdf", ".md")
    ext_imagens: tuple = (".png", ".jpg", ".jpeg", ".bmp")

    # --- Telemetria: detecção de anomalias ---
    # "auto" evita forçar uma fração fixa de anomalias em dados nominais.
    contaminacao_isolation_forest: str = "auto"
    z_score_limite: float = 4.0   # |z| acima disso = outlier estatístico real

    # --- Documentos: classificação de severidade ---
    # Palavras-chave que reforçam cada nível (apoio ao classificador ML)
    palavras_criticas: tuple = (
        "failure", "falha", "critical", "crítico", "abort", "emergency",
        "emergência", "loss", "perda", "overheat", "superaquecimento",
        "leak", "vazamento", "explosion", "explosão",
    )
    palavras_alerta: tuple = (
        "warning", "alerta", "aviso", "deviation", "desvio", "anomaly",
        "anomalia", "exceed", "excedeu", "degraded", "degradado",
    )

    # --- Imagens: visão computacional ---
    limiar_hotspot: int = 245        # brilho (0-255) acima disso = pixel saturado
    perc_hotspot_anomalia: float = 0.15  # % de pixels saturados p/ marcar anomalia

    # --- Nomes dos artefatos de saída ---
    arq_excel: str = "relatorio_missao.xlsx"
    arq_pdf: str = "relatorio_missao.pdf"
    arq_json: str = "resultado.json"
    arq_log: str = "execucao.log"

    def preparar_pastas(self):
        """Garante que as pastas do fluxo existam."""
        for p in (self.pasta_inbox, self.pasta_outputs, self.pasta_logs):
            p.mkdir(parents=True, exist_ok=True)
