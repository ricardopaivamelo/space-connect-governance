# Matriz de integração — Space Connect Governance

Classificação honesta do nível de integração de cada conexão do ecossistema.
A mesma matriz é gerada dentro de `data/integrated_snapshot.json` e exibida na
aba **Governança** do painel.

| Conexão | Estado | Detalhe |
|---|---|---|
| RPA → snapshot integrado | **Implementada e verificada** | `resultado.json` da execução local de 09/06/2026 é lido por `integration/build_snapshot.py` |
| Sensor neuromórfico → snapshot integrado | **Implementada e verificada** | comparação base × entrega reexecutada localmente; série do Ajuste B alimenta o painel |
| Snapshot → painel Streamlit | **Implementada e verificada** | `app.py` lê `data/integrated_snapshot.json` (testado com AppTest) |
| Painel → log de decisão humana | **Implementada e verificada** | decisões persistidas em `data/decision_log.jsonl` com timestamp, operador e justificativa |
| QML → snapshot integrado | Evidência auditada | métricas da reprodução local (5 seeds, leakage corrigido); sem vantagem quântica; não é detector operacional |
| Visão Computacional → snapshot integrado | Evidência auditada | métricas históricas do notebook (98,02% de acurácia em 6.268 imagens); modelo treinado não foi entregue |
| Recuperação semântica (PLN) → solução | Conceitual | busca documental auditada (31 chunks, FAISS, top-k); sem LLM, prompt ou interface |
| IoT → telemetria do ecossistema | Não recebida | módulo não entregue; slot reservado: ESP32/sensores → plataforma IoT → eventos → neuromórfico/RPA |

## Níveis usados

- `live` — componente executa em tempo real nesta solução.
- `replayed_evidence` — artefato regenerado por reexecução local verificada.
- `historical_notebook_output` — outputs gravados auditados, sem reexecução.
- `conceptual` — papel descrito na arquitetura, sem conexão técnica.
- `not_received` — material não entregue até o fechamento.
