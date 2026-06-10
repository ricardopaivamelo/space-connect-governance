"""
logger.py
=========
Configura o logging do robô: grava tanto no console quanto em um arquivo
em logs/, registrando cada etapa, sucesso e erro do fluxo. O log é uma
peça central do critério de "tratamento de exceções e integridade do fluxo".
"""

import logging
from pathlib import Path


def configurar_logger(pasta_logs: Path, arquivo: str) -> logging.Logger:
    pasta_logs.mkdir(parents=True, exist_ok=True)
    caminho = pasta_logs / arquivo

    logger = logging.getLogger("missionops")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()  # evita handlers duplicados em re-execuções

    formato = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    # Console
    console = logging.StreamHandler()
    console.setFormatter(formato)
    logger.addHandler(console)

    # Arquivo
    arquivo_handler = logging.FileHandler(caminho, mode="w", encoding="utf-8")
    arquivo_handler.setFormatter(formato)
    logger.addHandler(arquivo_handler)

    return logger
