"""Contrato do snapshot integrado.

Validacao leve, sem dependencias externas, para garantir que o JSON
consolidado sempre tenha os campos exigidos pela matriz de governanca.
"""
from __future__ import annotations

SNAPSHOT_REQUIRED_KEYS = [
    "generated_at",
    "solution_name",
    "scenario",
    "modules",
    "metrics",
    "alerts",
    "integration_matrix",
    "governance",
    "source_artifacts",
    "limitations",
]

MODULE_REQUIRED_KEYS = [
    "name",
    "discipline",
    "status",
    "verification_level",
    "integration_level",
    "data_origin",
    "evidence",
    "metrics",
    "limitations",
    "human_review_required",
]

VALID_DATA_ORIGINS = {
    "live",
    "replayed_evidence",
    "historical_notebook_output",
    "conceptual",
    "not_received",
}

ALERT_REQUIRED_KEYS = ["alert_id", "source_module", "severity", "title", "detail"]


class SnapshotValidationError(ValueError):
    pass


def validate_snapshot(snapshot: dict) -> list[str]:
    """Retorna a lista de erros encontrados. Lista vazia significa valido."""
    errors: list[str] = []
    for key in SNAPSHOT_REQUIRED_KEYS:
        if key not in snapshot:
            errors.append(f"campo obrigatorio ausente no snapshot: {key}")
    for module in snapshot.get("modules", []):
        name = module.get("name", "<sem nome>")
        for key in MODULE_REQUIRED_KEYS:
            if key not in module:
                errors.append(f"modulo {name}: campo obrigatorio ausente: {key}")
        origin = module.get("data_origin")
        if origin is not None and origin not in VALID_DATA_ORIGINS:
            errors.append(f"modulo {name}: data_origin invalido: {origin}")
    for alert in snapshot.get("alerts", []):
        for key in ALERT_REQUIRED_KEYS:
            if key not in alert:
                errors.append(f"alerta {alert.get('alert_id', '?')}: campo ausente: {key}")
    return errors


def assert_valid(snapshot: dict) -> None:
    errors = validate_snapshot(snapshot)
    if errors:
        raise SnapshotValidationError("; ".join(errors))
