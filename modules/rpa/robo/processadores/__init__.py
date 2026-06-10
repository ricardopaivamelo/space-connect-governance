"""Processadores de IA por tipo de dado (telemetria, documentos, imagens)."""

from .telemetria import processar_telemetria
from .documentos import processar_documento
from .imagens import processar_imagem

__all__ = ["processar_telemetria", "processar_documento", "processar_imagem"]
