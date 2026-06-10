"""
pipeline.py
===========
Orquestra o fluxo de ponta a ponta (o "robô" de RPA):

    inbox -> classificação -> processamento por IA -> consolidação -> artefatos

Princípios de engenharia aplicados (critério de Arquitetura de Fluxo):
  - Cada arquivo é processado isoladamente em um bloco try/except: uma falha
    em um item NÃO derruba o lote inteiro (resiliência).
  - Toda etapa e exceção é registrada no log.
  - Ao final, estatísticas consolidadas alimentam os artefatos e o dashboard.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from .config import Config
from .logger import configurar_logger
from . import loader
from .processadores import (
    processar_telemetria, processar_documento, processar_imagem,
)
from . import artefatos


PROCESSADORES = {
    "telemetria": processar_telemetria,
    "documento": processar_documento,
    "imagem": processar_imagem,
}


def executar(cfg: Config | None = None) -> Dict:
    """Executa o pipeline completo e retorna um relatório de execução."""
    cfg = cfg or Config()
    cfg.preparar_pastas()
    log = configurar_logger(cfg.pasta_logs, cfg.arq_log)

    inicio = datetime.now()
    log.info("=" * 60)
    log.info("INÍCIO DA EXECUÇÃO — MissionOps RPA")
    log.info("=" * 60)

    # --- Etapa 1: varrer e classificar ---
    arquivos = loader.varrer_inbox(cfg)
    log.info(f"Etapa 1 | {len(arquivos)} arquivo(s) reconhecido(s) no inbox.")
    if not arquivos:
        log.warning("Nenhum arquivo válido no inbox. Encerrando.")

    resultados: Dict[str, List[Dict]] = {
        "telemetria": [], "documentos": [], "imagens": [],
    }
    chave_saida = {"telemetria": "telemetria", "documento": "documentos",
                   "imagem": "imagens"}

    falhas: List[Dict] = []

    # --- Etapa 2: processar item a item, com error handling ---
    for arq in arquivos:
        try:
            loader.validar(arq)
            processador = PROCESSADORES[arq.tipo]
            resultado = processador(arq.caminho, cfg)
            resultados[chave_saida[arq.tipo]].append(resultado)
            log.info(f"  OK   [{arq.tipo}] {arq.nome} -> {resultado['severidade']}")
        except Exception as e:
            # Resiliência: registra a falha e segue para o próximo arquivo
            falhas.append({"arquivo": arq.nome, "tipo": arq.tipo,
                           "erro": f"{type(e).__name__}: {e}"})
            log.error(f"  FALHA [{arq.tipo}] {arq.nome} -> {type(e).__name__}: {e}")

    # --- Etapa 3: estatísticas consolidadas ---
    estatisticas = {
        "total_arquivos": len(arquivos),
        "total_processados": sum(len(v) for v in resultados.values()),
        "total_falhas": len(falhas),
        "telemetria_criticas": sum(
            1 for r in resultados["telemetria"] if r["severidade"] == "CRÍTICO"),
        "documentos_criticos": sum(
            1 for r in resultados["documentos"]
            if r["severidade"] in ("CRÍTICO", "ALERTA")),
        "imagens_anomalas": sum(
            1 for r in resultados["imagens"] if r["severidade"] == "ANOMALIA"),
        "falhas": falhas,
    }
    log.info(
        f"Etapa 3 | Processados {estatisticas['total_processados']}, "
        f"falhas {estatisticas['total_falhas']}.")

    # --- Etapa 4: gerar artefatos (cada um protegido por try/except) ---
    artefatos_gerados = {}
    for nome, funcao in (
        ("excel", lambda: artefatos.gerar_excel(resultados, cfg)),
        ("json", lambda: artefatos.gerar_json(resultados, estatisticas, cfg)),
        ("pdf", lambda: artefatos.gerar_pdf(resultados, estatisticas, cfg)),
    ):
        try:
            caminho = funcao()
            artefatos_gerados[nome] = str(caminho)
            log.info(f"Etapa 4 | Artefato '{nome}' gerado: {caminho.name}")
        except Exception as e:
            log.error(f"Etapa 4 | Falha ao gerar '{nome}': {type(e).__name__}: {e}")

    duracao = (datetime.now() - inicio).total_seconds()
    log.info(f"FIM DA EXECUÇÃO — {duracao:.2f}s")
    log.info("=" * 60)

    return {
        "estatisticas": estatisticas,
        "artefatos": artefatos_gerados,
        "duracao_segundos": round(duracao, 2),
    }
