import subprocess
import sys
from pathlib import Path

from streamlit.testing.v1 import AppTest

REPO_ROOT = Path(__file__).resolve().parents[1]


def setup_module(module):
    subprocess.run(
        [sys.executable, str(REPO_ROOT / "integration" / "build_snapshot.py")],
        check=True, cwd=REPO_ROOT,
    )


def test_app_runs_without_exception():
    at = AppTest.from_file(str(REPO_ROOT / "app.py"), default_timeout=30)
    at.run()
    assert not at.exception
    assert "Space Connect Governance" in at.title[0].value


def test_app_reads_snapshot_metrics():
    at = AppTest.from_file(str(REPO_ROOT / "app.py"), default_timeout=30)
    at.run()
    metric_labels = [m.label for m in at.metric]
    assert "Modulos no ecossistema" in metric_labels
    values = {m.label: m.value for m in at.metric}
    assert values["Modulos no ecossistema"] == "7"
