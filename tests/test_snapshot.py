import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from integration import schema  # noqa: E402
from integration.build_snapshot import build_snapshot  # noqa: E402


def test_build_snapshot_is_valid():
    snapshot = build_snapshot()
    assert schema.validate_snapshot(snapshot) == []


def test_snapshot_has_seven_modules_and_honest_levels():
    snapshot = build_snapshot()
    assert len(snapshot["modules"]) == 7
    by_discipline = {m["discipline"]: m for m in snapshot["modules"]}
    assert by_discipline["Physical Computing, Embedded AI, Robotics e Cognitive IoT"]["data_origin"] == "not_received"
    assert by_discipline["PLN, Chatbots e Virtual Agents"]["integration_level"] == "conceptual"
    assert by_discipline["Visao Computacional"]["metrics"]["accuracy"] == 0.9802


def test_alerts_have_required_fields_and_rpa_criticals():
    snapshot = build_snapshot()
    assert snapshot["alerts"], "snapshot deve consolidar alertas"
    for alert in snapshot["alerts"]:
        for key in schema.ALERT_REQUIRED_KEYS:
            assert key in alert
    rpa_alerts = [a for a in snapshot["alerts"] if a["source_module"] == "MissionOps RPA"]
    assert len(rpa_alerts) >= 4  # 1 telemetria critica + 2 documentos + 1 imagem


def test_cli_generates_file_and_validates(tmp_path):
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "integration" / "build_snapshot.py")],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stderr
    data = json.loads((REPO_ROOT / "data" / "integrated_snapshot.json").read_text(encoding="utf-8"))
    assert data["solution_name"] == "Space Connect Governance"
