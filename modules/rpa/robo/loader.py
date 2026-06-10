"""
loader.py
=========
Etapa 1 do fluxo (RPA): varre a pasta de entrada (inbox), identifica o
tipo de cada arquivo (telemetria, documento ou imagem) pela extensão e
faz uma validação básica (arquivo existe, não está vazio).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from .config import Config


@dataclass
class ArquivoEntrada:
    caminho: Path
    tipo: str          # "telemetria" | "documento" | "imagem"
    nome: str
    tamanho_bytes: int


def classificar_tipo(caminho: Path, cfg: Config) -> str | None:
    ext = caminho.suffix.lower()
    if ext in cfg.ext_telemetria:
        return "telemetria"
    if ext in cfg.ext_documentos:
        return "documento"
    if ext in cfg.ext_imagens:
        return "imagem"
    return None


def varrer_inbox(cfg: Config) -> List[ArquivoEntrada]:
    """Lista e classifica os arquivos válidos do inbox."""
    arquivos: List[ArquivoEntrada] = []
    if not cfg.pasta_inbox.exists():
        return arquivos

    for caminho in sorted(cfg.pasta_inbox.iterdir()):
        if not caminho.is_file():
            continue
        if caminho.name.startswith("."):
            continue  # ignora ocultos
        tipo = classificar_tipo(caminho, cfg)
        if tipo is None:
            continue  # extensão não suportada
        tamanho = caminho.stat().st_size
        arquivos.append(
            ArquivoEntrada(
                caminho=caminho, tipo=tipo, nome=caminho.name,
                tamanho_bytes=tamanho,
            )
        )
    return arquivos


def validar(arquivo: ArquivoEntrada) -> None:
    """Valida um arquivo de entrada. Lança ValueError se inválido."""
    if not arquivo.caminho.exists():
        raise ValueError(f"Arquivo não encontrado: {arquivo.nome}")
    if arquivo.tamanho_bytes == 0:
        raise ValueError(f"Arquivo vazio: {arquivo.nome}")
