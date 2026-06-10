"""Registro auditavel de decisoes humanas.

Cada decisao vira uma linha JSON em data/decision_log.jsonl com timestamp,
operador, alerta, decisao e justificativa. Diferente do prototipo original
do Front-End, o registro sobrevive ao fim da sessao.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG_PATH = REPO_ROOT / "data" / "decision_log.jsonl"

VALID_DECISIONS = {"APROVADO", "REJEITADO"}


def build_decision_record(
    alert_id: str,
    decision: str,
    operator: str,
    justification: str,
    source_module: str = "",
    snapshot_generated_at: str = "",
) -> dict:
    if decision not in VALID_DECISIONS:
        raise ValueError(f"decisao invalida: {decision}")
    if not operator.strip():
        raise ValueError("operador obrigatorio")
    if not justification.strip():
        raise ValueError("justificativa obrigatoria")
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "alert_id": alert_id,
        "source_module": source_module,
        "decision": decision,
        "operator": operator.strip(),
        "justification": justification.strip(),
        "snapshot_generated_at": snapshot_generated_at,
    }


def append_decision(record: dict, log_path: Path = DEFAULT_LOG_PATH) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_decisions(log_path: Path = DEFAULT_LOG_PATH) -> list[dict]:
    if not log_path.exists():
        return []
    decisions = []
    with log_path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                decisions.append(json.loads(line))
    return decisions
