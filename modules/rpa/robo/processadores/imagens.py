"""
processadores/imagens.py
========================
Visão Computacional aplicada a imagens de sensores/orbitais
(PNG, JPG, BMP).

Sem depender de modelos pesados, usa técnicas clássicas de CV:
  - converte para escala de cinza e calcula estatísticas (brilho médio,
    desvio, contraste);
  - detecta "hotspots" (pixels muito brilhantes), úteis para sinalizar
    focos de calor / saturação de sensor / anomalias luminosas;
  - estima nitidez pela variância do Laplaciano (imagem borrada vs nítida);
  - classifica a imagem como NOMINAL ou ANOMALIA conforme o % de hotspots.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
from PIL import Image

from ..config import Config


def _variancia_laplaciano(cinza: np.ndarray) -> float:
    """Mede nitidez: variância da resposta a um kernel Laplaciano 3x3."""
    k = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)
    h, w = cinza.shape
    if h < 3 or w < 3:
        return 0.0
    # convolução "válida" simples
    regiao = np.lib.stride_tricks.sliding_window_view(cinza, (3, 3))
    resp = np.tensordot(regiao, k, axes=([2, 3], [0, 1]))
    return float(resp.var())


def processar_imagem(caminho: Path, cfg: Config) -> Dict:
    with Image.open(caminho) as img:
        img = img.convert("RGB")
        largura, altura = img.size
        cinza = np.asarray(img.convert("L"), dtype=np.float32)

    total_pixels = cinza.size
    brilho_medio = float(cinza.mean())
    desvio = float(cinza.std())
    contraste = float(cinza.max() - cinza.min())

    # Hotspots: pixels acima do limiar de brilho
    mascara_hot = cinza >= cfg.limiar_hotspot
    n_hot = int(mascara_hot.sum())
    perc_hot = round(100 * n_hot / total_pixels, 3)

    nitidez = round(_variancia_laplaciano(cinza), 2)

    anomalia = perc_hot >= cfg.perc_hotspot_anomalia
    severidade = "ANOMALIA" if anomalia else "NOMINAL"

    return {
        "nome": caminho.name,
        "tipo": "imagem",
        "largura": largura,
        "altura": altura,
        "brilho_medio": round(brilho_medio, 2),
        "desvio_brilho": round(desvio, 2),
        "contraste": round(contraste, 2),
        "nitidez": nitidez,
        "perc_hotspots": perc_hot,
        "severidade": severidade,
        "resumo": (
            f"{largura}x{altura}px; brilho médio {brilho_medio:.0f}; "
            f"{perc_hot}% de hotspots -> {severidade}."
        ),
    }
