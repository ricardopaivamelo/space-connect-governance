# Arquitetura integradora

```text
                          [Physical Computing/IoT - NÃO RECEBIDO]
                          ESP32/sensores -> plataforma IoT (slot reservado)
                                          |
                                          v
  dataset oficial 61 leituras   ->  Sensor neuromórfico (reexecutado)
                                          |  eventos/transições
                                          v
  CSVs, logs, docs, imagens    ->   MissionOps RPA (executado localmente)
                                          |  resultado.json
                                          v
                            integration/build_snapshot.py
                                          |
                 +------------------------+-------------------------+
                 |                        |                         |
   QML (reproduzido, 5 seeds)   Visão (outputs auditados)   PLN (recuperação
   evidência comparativa        métricas reais 98,02%       semântica, 31 chunks)
                 |                        |                         |
                 +------------------------+-------------------------+
                                          v
                          data/integrated_snapshot.json
                          (contrato validado por schema.py)
                                          |
                                          v
                              app.py (painel Streamlit)
                     Panorama | Módulos | Sensor | Decisão | Governança
                                          |
                                          v
                          decisão humana com operador
                          e justificativa obrigatórios
                                          |
                                          v
                          data/decision_log.jsonl (auditável)
```

## Fluxo da integração mínima real

1. `build_snapshot.py` lê apenas artefatos verificados em `integration/sources/`.
2. O snapshot é validado contra o contrato (`schema.py`) — falha gera exit code ≠ 0.
3. O painel lê o JSON e exibe origem, status, métrica e nível de integração por módulo.
4. Cada alerta exige decisão humana com operador e justificativa.
5. A decisão é persistida em `decision_log.jsonl` com timestamp UTC.
