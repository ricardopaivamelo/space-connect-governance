"""
processadores/documentos.py
===========================
IA/NLP aplicada a logs e relatórios técnicos (TXT, LOG, PDF, MD).

Faz duas coisas:
  1. Classifica a SEVERIDADE do documento (NOMINAL / ALERTA / CRÍTICO) com um
     classificador de Machine Learning (TF-IDF + Regressão Logística),
     treinado em exemplos sintéticos rotulados embutidos no código. Um reforço
     por palavras-chave aumenta a robustez.
  2. Extrai ENTIDADES técnicas por expressões regulares: datas/horas, códigos
     de erro, subsistemas citados e percentuais.

O classificador é treinado uma única vez por execução (cacheado).
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Dict, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from ..config import Config
from pypdf import PdfReader

# ---------------------------------------------------------------------------
# Dados de treino sintéticos para o classificador de severidade
# (frases típicas de logs de missão, em PT e EN)
# ---------------------------------------------------------------------------
TREINO = [
    # NOMINAL
    ("all systems nominal telemetry within expected range", "NOMINAL"),
    ("rotina de verificação concluída sem ocorrências", "NOMINAL"),
    ("battery charge stable communication link healthy", "NOMINAL"),
    ("manobra orbital executada conforme planejado", "NOMINAL"),
    ("sensor calibration completed successfully", "NOMINAL"),
    ("temperatura dentro dos limites operacionais normais", "NOMINAL"),
    ("data downlink finished no errors reported", "NOMINAL"),
    ("checagem diária dos subsistemas ok", "NOMINAL"),
    # ALERTA
    ("warning solar panel output slightly below expected", "ALERTA"),
    ("alerta leve desvio de temperatura no subsistema térmico", "ALERTA"),
    ("communication latency exceeded nominal threshold", "ALERTA"),
    ("aviso degradação gradual da bateria detectada", "ALERTA"),
    ("minor deviation in attitude control observed", "ALERTA"),
    ("anomalia de leitura intermitente no giroscópio", "ALERTA"),
    ("signal strength degraded monitor closely", "ALERTA"),
    ("pressão do tanque excedeu faixa recomendada", "ALERTA"),
    # CRÍTICO
    ("critical failure in propulsion system abort sequence", "CRÍTICO"),
    ("falha crítica perda de comunicação com a sonda", "CRÍTICO"),
    ("overheat detected emergency shutdown initiated", "CRÍTICO"),
    ("vazamento de combustível detectado risco de explosão", "CRÍTICO"),
    ("loss of attitude control spacecraft tumbling", "CRÍTICO"),
    ("superaquecimento crítico do reator desligamento de emergência", "CRÍTICO"),
    ("power system total failure mission at risk", "CRÍTICO"),
    ("falha catastrófica no sistema de suporte à vida", "CRÍTICO"),
]


@lru_cache(maxsize=1)
def _treinar_classificador() -> Pipeline:
    textos = [t for t, _ in TREINO]
    rotulos = [r for _, r in TREINO]
    modelo = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
        ("clf", LogisticRegression(max_iter=1000)),
    ])
    modelo.fit(textos, rotulos)
    return modelo


def _ler_texto(caminho: Path) -> str:
    if caminho.suffix.lower() == ".pdf":
        reader = PdfReader(str(caminho))
        return "\n".join((p.extract_text() or "") for p in reader.pages)
    return caminho.read_text(encoding="utf-8", errors="ignore")


def _extrair_entidades(texto: str) -> Dict[str, List[str]]:
    """Extrai entidades técnicas do log via regex."""
    datas = re.findall(
        r"\b\d{4}-\d{2}-\d{2}(?:[ T]\d{2}:\d{2}(?::\d{2})?)?\b", texto)
    codigos_erro = re.findall(r"\b(?:ERR|ERROR|ERRO|CODE|E)[-_ ]?\d{2,5}\b",
                              texto, flags=re.IGNORECASE)
    percentuais = re.findall(r"\b\d{1,3}(?:[.,]\d+)?\s?%", texto)
    # subsistemas comuns de missão espacial
    subsistemas_conhecidos = [
        "propulsion", "propulsão", "battery", "bateria", "thermal", "térmico",
        "communication", "comunicação", "navigation", "navegação", "power",
        "energia", "attitude", "atitude", "payload", "sensor", "reactor",
        "reator", "fuel", "combustível",
    ]
    achados = sorted({
        s for s in subsistemas_conhecidos
        if re.search(rf"\b{s}\b", texto, flags=re.IGNORECASE)
    })
    return {
        "datas": sorted(set(datas))[:10],
        "codigos_erro": sorted(set(c.upper() for c in codigos_erro))[:10],
        "percentuais": sorted(set(percentuais))[:10],
        "subsistemas": achados,
    }


def _reforco_palavras_chave(texto: str, cfg: Config) -> str | None:
    t = texto.lower()
    if any(p in t for p in cfg.palavras_criticas):
        return "CRÍTICO"
    if any(p in t for p in cfg.palavras_alerta):
        return "ALERTA"
    return None


def processar_documento(caminho: Path, cfg: Config) -> Dict:
    texto = _ler_texto(caminho)
    if not texto.strip():
        raise ValueError("Documento sem texto extraível (possível PDF de imagem).")

    modelo = _treinar_classificador()
    severidade_ml = modelo.predict([texto])[0]

    # Reforço por palavras-chave: se houver termo crítico explícito, prevalece
    reforco = _reforco_palavras_chave(texto, cfg)
    if reforco == "CRÍTICO":
        severidade = "CRÍTICO"
    elif reforco == "ALERTA" and severidade_ml == "NOMINAL":
        severidade = "ALERTA"
    else:
        severidade = severidade_ml

    entidades = _extrair_entidades(texto)
    palavras = len(texto.split())

    return {
        "nome": caminho.name,
        "tipo": "documento",
        "palavras": palavras,
        "severidade": severidade,
        "severidade_modelo_ml": severidade_ml,
        "entidades": entidades,
        "resumo": (
            f"{palavras} palavras; severidade {severidade}; "
            f"{len(entidades['codigos_erro'])} código(s) de erro, "
            f"{len(entidades['subsistemas'])} subsistema(s) citado(s)."
        ),
    }
