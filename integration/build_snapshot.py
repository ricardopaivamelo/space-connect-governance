"""Gera o snapshot integrado da solucao Space Connect Governance.

Le somente artefatos verificados em integration/sources/ e consolida em
data/integrated_snapshot.json, com nivel de verificacao e origem de dados
declarados por modulo. O script falha com exit code != 0 se o snapshot
nao validar contra o contrato em schema.py.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from integration import schema
else:
    from . import schema

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCES = REPO_ROOT / "integration" / "sources"
OUTPUT = REPO_ROOT / "data" / "integrated_snapshot.json"

SOLUTION_NAME = "Space Connect Governance"
SCENARIO = (
    "Plataforma integrada de monitoramento e apoio a decisao para ambientes "
    "extremos e riscos ambientais, usando dados espaciais, processamento "
    "inteligente e supervisao humana."
)


def load_json(name: str) -> dict:
    return json.loads((SOURCES / name).read_text(encoding="utf-8"))


def build_rpa_module(rpa: dict) -> dict:
    stats = rpa["estatisticas"]
    return {
        "name": "MissionOps RPA",
        "discipline": "AI for RPA",
        "status": "executado e verificado localmente em 09/06/2026",
        "verification_level": "verified_local_execution",
        "integration_level": "integrated_data_source",
        "data_origin": "replayed_evidence",
        "evidence": ["evidence/rpa/resultado.json", "evidence/rpa/execucao.log"],
        "metrics": {
            "total_arquivos": stats["total_arquivos"],
            "total_processados": stats["total_processados"],
            "total_falhas": stats["total_falhas"],
            "telemetria_criticas": stats["telemetria_criticas"],
            "documentos_criticos": stats["documentos_criticos"],
            "imagens_anomalas": stats["imagens_anomalas"],
        },
        "limitations": [
            "classificador NLP sintetico com acuracia de 41,7% e recall zero para ALERTA (nao reaproveitado)",
            "analise de imagem usa proxy de brilho/saturacao, nao detector semantico de incendio",
            "regras por substring podem gerar falso positivo em negacao",
            "logs sobrescritos a cada execucao e ausencia de testes automatizados",
            "a entrega oficial da disciplina (notebook GS_RPA, em modules/rpa/entrega_disciplina/) e um artefato standalone com dataset sintetico de 5.000 registros gerado em codigo; nao foi integrada ao snapshot",
        ],
        "human_review_required": True,
    }


def build_iot_module(iot: dict) -> dict:
    return {
        "name": "AgroSat Monitor (Physical Computing / IoT)",
        "discipline": "Physical Computing, Embedded AI, Robotics e Cognitive IoT",
        "status": "incorporado ao repositorio em 09/06/2026; codigo revisado; integracao ao snapshot prevista como evolucao",
        "verification_level": "code_audited_not_executed",
        "integration_level": "not_integrated",
        "data_origin": "received_late",
        "evidence": ["modules/iot/iot-agro-space/"],
        "metrics": {
            "firmware_lines": 612,
            "mqtt_topics": 5,
            "docker_services": 4,
        },
        "limitations": iot["audit_issues"]
        + [
            "integracao tecnica nao realizada: chegada posterior ao fechamento do pacote integrado",
            "telemetria atual da plataforma segue simulada, originada dos demais modulos",
        ],
        "human_review_required": True,
    }


def build_neuromorphic_module(comp: dict) -> dict:
    by_label = {c["ajuste"]: c for c in comp["comparacoes"]}
    a, b = by_label["A_entrega"], by_label["B_entrega"]
    return {
        "name": "NeuroSpace Alert (sensor neuromorfico simulado)",
        "discipline": "Computacao Neuromorfica",
        "status": "reexecutado localmente com o dataset recebido em 09/06/2026",
        "verification_level": "verified_local_execution",
        "integration_level": "integrated_data_source",
        "data_origin": "replayed_evidence",
        "evidence": [
            "evidence/neuromorfico/",
            "integration/sources/neuromorphic_comparacao.json",
            "integration/sources/neuromorphic_saida_ajuste_b.csv",
        ],
        "metrics": {
            "dataset_rows": comp["dataset_rows"],
            "ajuste_A_entrega_accuracy": a["accuracy_vs_condicao_real"],
            "ajuste_B_entrega_accuracy": b["accuracy_vs_condicao_real"],
            "ajuste_A_primeiro_amarelo_min": a["primeiro_nao_apagado_min"],
            "ajuste_A_primeiro_vermelho_min": a["primeiro_vermelho_min"],
            "ajuste_B_primeiro_amarelo_min": b["primeiro_nao_apagado_min"],
            "ajuste_B_primeiro_vermelho_min": b["primeiro_vermelho_min"],
        },
        "limitations": [
            "PDF do grupo cita limiares 250/290/330, mas o codigo usa 25/29/33",
            "atualizacao do estado nao usa delta_t: o resultado depende da frequencia de amostragem",
            "economia de energia proposta, nao medida",
            "recomendacao do Ajuste B nao e sustentada pela comparacao com condicao_real (Ajuste A tem acuracia maior e menos atraso)",
        ],
        "human_review_required": True,
    }


def build_qml_module(qml: dict) -> dict:
    return {
        "name": "Deteccao de anomalias com QML",
        "discipline": "Computacao Quantica e IA",
        "status": "reproduzido localmente com correcao de leakage e cinco seeds",
        "verification_level": "verified_local_execution",
        "integration_level": "evidence_only",
        "data_origin": "replayed_evidence",
        "evidence": ["evidence/qml/"],
        "metrics": {
            "svm_mean_accuracy": qml["corrected_run_5_seeds"]["svm_mean_accuracy"],
            "qsvc_mean_accuracy": qml["corrected_run_5_seeds"]["qsvc_mean_accuracy"],
            "majority_baseline_accuracy": qml["corrected_run_5_seeds"]["majority_baseline_accuracy"],
        },
        "limitations": [
            "sem vantagem quantica observada; QSVC abaixo do SVM classico",
            "execucao simulada localmente, sem hardware quantico e sem modelo de ruido",
            "uso recomendado: estudo comparativo e evidencia de governanca, nao detector operacional",
        ],
        "human_review_required": True,
    }


def build_vision_module(vision: dict) -> dict:
    return {
        "name": "Classificador de risco de incendio (wildfire)",
        "discipline": "Visao Computacional",
        "status": "outputs historicos do notebook auditados, sem reexecucao do treinamento",
        "verification_level": "audited_outputs",
        "integration_level": "evidence_only",
        "data_origin": "historical_notebook_output",
        "evidence": ["evidence/visao/"],
        "metrics": vision["metrics"],
        "limitations": vision["limitations"]
        + [vision["divergences"], "autoria em correcao junto ao integrante responsavel"],
        "human_review_required": True,
    }


def build_rag_module(rag: dict) -> dict:
    return {
        "name": "Recuperacao semantica documental",
        "discipline": "PLN, Chatbots e Virtual Agents",
        "status": "componente de recuperacao auditado; camada generativa nao implementada",
        "verification_level": "audited_outputs",
        "integration_level": "conceptual",
        "data_origin": "historical_notebook_output",
        "evidence": ["evidence/rag/"],
        "metrics": {"chunks_indexed": rag["chunks_indexed"]},
        "limitations": [
            "nao ha LLM, prompt, interface nem comparacao RAG x LLM puro",
            "corpus de dez PDFs nao fornecido",
            "declaracoes de Llama 3.2 3B e 90% de assertividade nao tem evidencia no notebook e nao sao repetidas aqui",
        ],
        "human_review_required": True,
    }


def build_frontend_module(front: dict) -> dict:
    return {
        "name": "Painel integrado de decisao (este repositorio)",
        "discipline": "Front-End e Mobile Development",
        "status": "adaptado do GeoGuard IA para consumir o snapshot integrado",
        "verification_level": "verified_local_execution",
        "integration_level": "integrated_ui",
        "data_origin": "live",
        "evidence": ["app.py", "evidence/frontend/frontend_metrics.json"],
        "metrics": {
            "registros_simulados_originais": front["linhas"],
            "alertas_criticos_simulados": front["metricas"]["alertas_criticos"],
        },
        "limitations": [
            "indicador original de populacao exposta somava pessoa-dias (inflacao ~30,9x) e nao e usado como resultado",
            "dados climaticos do prototipo original sao sinteticos; o painel integrado le apenas artefatos verificados",
        ],
        "human_review_required": True,
    }


def build_alerts(rpa: dict, comp: dict) -> list[dict]:
    alerts = []
    for item in rpa["resultados"]["telemetria"]:
        if item["severidade"] != "NOMINAL":
            alerts.append({
                "alert_id": f"rpa-tel-{item['nome']}",
                "source_module": "MissionOps RPA",
                "severity": item["severidade"],
                "title": f"Telemetria {item['nome']}",
                "detail": item["resumo"],
            })
    for item in rpa["resultados"]["documentos"]:
        if item["severidade"] in {"ALERTA", "CRÍTICO", "CRITICO"}:
            alerts.append({
                "alert_id": f"rpa-doc-{item['nome']}",
                "source_module": "MissionOps RPA",
                "severity": item["severidade"],
                "title": f"Documento {item['nome']}",
                "detail": item["resumo"],
            })
    for item in rpa["resultados"]["imagens"]:
        if item["severidade"] != "NOMINAL":
            alerts.append({
                "alert_id": f"rpa-img-{item['nome']}",
                "source_module": "MissionOps RPA",
                "severity": item["severidade"],
                "title": f"Imagem {item['nome']}",
                "detail": item["resumo"],
            })
    b = next(c for c in comp["comparacoes"] if c["ajuste"] == "B_entrega")
    alerts.append({
        "alert_id": "neuro-b-vermelho",
        "source_module": "NeuroSpace Alert",
        "severity": "CRÍTICO",
        "title": "Transicao para ALERTA_CRITICO no Ajuste B",
        "detail": (
            f"Sensor neuromorfico (Ajuste B da entrega) atinge estado vermelho aos "
            f"{b['primeiro_vermelho_min']} min; condicao CRITICA real comeca aos 200 min "
            f"(atraso de {b['primeiro_vermelho_min'] - 200} min)."
        ),
    })
    return alerts


def build_integration_matrix() -> list[dict]:
    return [
        {"connection": "RPA -> snapshot integrado", "status": "implemented_verified",
         "detail": "resultado.json da execucao local e lido por build_snapshot.py"},
        {"connection": "Sensor neuromorfico -> snapshot integrado", "status": "implemented_verified",
         "detail": "comparacao reexecutada e serie do Ajuste B sao lidas por build_snapshot.py"},
        {"connection": "Snapshot integrado -> painel Streamlit", "status": "implemented_verified",
         "detail": "app.py le data/integrated_snapshot.json e exibe modulos, metricas e alertas"},
        {"connection": "Painel -> log de decisao humana", "status": "implemented_verified",
         "detail": "decisoes sao persistidas em data/decision_log.jsonl com timestamp, operador e justificativa"},
        {"connection": "QML -> snapshot integrado", "status": "evidence_only",
         "detail": "metricas da reproducao auditada entram como evidencia comparativa, nao como detector operacional"},
        {"connection": "Visao Computacional -> snapshot integrado", "status": "evidence_only",
         "detail": "metricas historicas do notebook auditado; modelo treinado nao foi entregue"},
        {"connection": "Recuperacao semantica (PLN) -> solucao", "status": "conceptual",
         "detail": "componente de busca documental auditado; sem camada generativa ou interface"},
        {"connection": "IoT -> telemetria do ecossistema", "status": "not_integrated",
         "detail": "AgroSat Monitor incorporado ao repositorio em 09/06 (ESP32/Wokwi + MQTT + Node-RED + InfluxDB + Grafana); codigo revisado; integracao tecnica prevista como evolucao da plataforma"},
    ]


def build_snapshot() -> dict:
    rpa = load_json("rpa_resultado.json")
    comp = load_json("neuromorphic_comparacao.json")
    qml = load_json("qml_metrics.json")
    vision = load_json("vision_metrics.json")
    rag = load_json("rag_status.json")
    iot = load_json("iot_status.json")
    front = load_json("frontend_metrics.json")

    modules = [
        build_rpa_module(rpa),
        build_iot_module(iot),
        build_neuromorphic_module(comp),
        build_qml_module(qml),
        build_vision_module(vision),
        build_rag_module(rag),
        build_frontend_module(front),
    ]
    alerts = build_alerts(rpa, comp)

    integrated_levels = {"integrated_data_source", "integrated_ui"}
    snapshot = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "solution_name": SOLUTION_NAME,
        "scenario": SCENARIO,
        "modules": modules,
        "metrics": {
            "modules_total": len(modules),
            "modules_integrated": sum(1 for m in modules if m["integration_level"] in integrated_levels),
            "modules_evidence_only": sum(1 for m in modules if m["integration_level"] == "evidence_only"),
            "modules_conceptual": sum(1 for m in modules if m["integration_level"] == "conceptual"),
            "modules_not_received": sum(1 for m in modules if m["data_origin"] == "not_received"),
            "modules_received_late": sum(1 for m in modules if m["data_origin"] == "received_late"),
            "alerts_total": len(alerts),
            "rpa_files_processed": rpa["estatisticas"]["total_processados"],
            "rpa_failures_handled": rpa["estatisticas"]["total_falhas"],
        },
        "alerts": alerts,
        "integration_matrix": build_integration_matrix(),
        "governance": {
            "human_in_the_loop": "alertas exigem decisao humana registrada em data/decision_log.jsonl",
            "credentials": "credencial Kaggle exposta no notebook original de Visao foi removida da copia de trabalho; revogacao solicitada ao titular; o segredo nao esta neste repositorio",
            "authorship_pending": "Visao Computacional lista autoria em correcao junto ao integrante responsavel",
            "ai_usage": "IA foi usada como ferramenta de auditoria, integracao e redacao tecnica; a conclusao do relatorio e de responsabilidade dos integrantes",
            "truthfulness": "cada modulo declara verification_level, integration_level e data_origin; metricas nao comprovadas nao sao apresentadas como resultado",
        },
        "source_artifacts": sorted(p.name for p in SOURCES.iterdir() if p.is_file()),
        "limitations": [
            "nenhum modelo roda ao vivo no painel: o snapshot consolida artefatos verificados (replayed/historical)",
            "modulo IoT incorporado ao repositorio em 09/06; codigo revisado; integracao tecnica prevista como evolucao da plataforma; telemetria segue simulada",
            "RAG generativo nao implementado; apenas recuperacao semantica auditada; corpus original de dez PDFs (edificacoes sustentaveis) segue ausente — quatro PDFs alternativos de tema espacial recebidos em 09/06 nao foram indexados",
            "metricas de Visao valem para o dataset canadense avaliado no notebook (6.268 imagens), sem teste geografico externo",
        ],
    }
    return snapshot


def main() -> int:
    snapshot = build_snapshot()
    errors = schema.validate_snapshot(snapshot)
    if errors:
        for error in errors:
            print(f"ERRO: {error}", file=sys.stderr)
        return 1
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"snapshot valido gerado em {OUTPUT.relative_to(REPO_ROOT)}")
    print(f"modulos: {snapshot['metrics']['modules_total']} | alertas: {snapshot['metrics']['alerts_total']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
