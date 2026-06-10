import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from integration.decision_log import append_decision, build_decision_record, read_decisions  # noqa: E402


def test_record_requires_operator_and_justification():
    with pytest.raises(ValueError):
        build_decision_record("a1", "APROVADO", "", "ok")
    with pytest.raises(ValueError):
        build_decision_record("a1", "APROVADO", "Ricardo", "  ")
    with pytest.raises(ValueError):
        build_decision_record("a1", "TALVEZ", "Ricardo", "ok")


def test_decision_is_persisted_and_read_back(tmp_path):
    log_path = tmp_path / "decision_log.jsonl"
    record = build_decision_record(
        "rpa-doc-emergencia_sol_003.log", "APROVADO", "Ricardo", "Confirmado com a telemetria",
        source_module="MissionOps RPA", snapshot_generated_at="2026-06-09T00:00:00+00:00",
    )
    append_decision(record, log_path)
    append_decision(build_decision_record("neuro-b-vermelho", "REJEITADO", "Pedro", "Falso positivo"), log_path)
    decisions = read_decisions(log_path)
    assert len(decisions) == 2
    assert decisions[0]["decision"] == "APROVADO"
    assert decisions[1]["decision"] == "REJEITADO"
    assert decisions[0]["timestamp"]
    assert decisions[0]["operator"] == "Ricardo"
