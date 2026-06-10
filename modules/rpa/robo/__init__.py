"""MissionOps RPA — robô de triagem e análise multimodal de dados de missão."""

from .config import Config
from .pipeline import executar

__all__ = ["Config", "executar"]
