# Space Connect Governance

Entrega integradora de **Governança em IA e Business Analytics** — Global
Solution 2026.1 (FIAP, curso de Inteligência Artificial). Tema: **Space
Connect — tecnologia espacial aplicada a desafios reais**.

> Plataforma integrada de monitoramento e apoio à decisão para ambientes
> extremos e riscos ambientais, usando dados espaciais, processamento
> inteligente e supervisão humana.

## Integrantes

| Nome | RM |
|---|---|
| Ricardo de Paiva Melo | 565522 |
| Pedro Leal Murad | 565460 |
| Jonas Alaf | 566479 |

Turma: 2TIAP(F-Y)-2026 · Professor de GBA: Marco Fontoura

## O que este repositório demonstra

Uma **integração mínima real e verificada** entre os módulos do semestre:

```text
artefatos verificados dos módulos
        -> integration/build_snapshot.py   (valida contrato em schema.py)
        -> data/integrated_snapshot.json
        -> app.py (painel Streamlit)
        -> decisão humana com operador e justificativa
        -> data/decision_log.jsonl (trilha auditável)
```

Cada módulo declara `verification_level`, `integration_level` e `data_origin`
(`live`, `replayed_evidence`, `historical_notebook_output`, `conceptual`,
`not_received`). Nenhuma métrica não comprovada é apresentada como resultado.
Detalhes em [`docs/integration_matrix.md`](docs/integration_matrix.md) e
[`docs/limitations.md`](docs/limitations.md).

## Estado dos módulos

| Disciplina | Módulo | Integração | Verificação |
|---|---|---|---|
| AI for RPA | MissionOps RPA | Integrado (fonte de dados) | Executado localmente em 09/06/2026 |
| Physical Computing/IoT | — | Não recebido | Slot arquitetural reservado |
| Computação Neuromórfica | NeuroSpace Alert | Integrado (fonte de dados) | Reexecutado com o dataset oficial |
| Computação Quântica e IA | SVM × QSVC | Evidência auditada | Reproduzido (5 seeds, leakage corrigido) |
| Visão Computacional | Classificador wildfire | Evidência auditada | Outputs históricos auditados |
| PLN, Chatbots e Virtual Agents | Recuperação semântica | Conceitual | Notebook auditado (sem LLM) |
| Front-End | Painel integrado (este repo) | Integrado (interface) | AppTest sem exceções |

## Como executar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 1. gerar o snapshot integrado (valida o contrato; falha => exit code != 0)
python integration/build_snapshot.py

# 2. abrir o painel
streamlit run app.py

# 3. rodar os testes
python -m pytest -q
```

## Estrutura

```text
app.py                  painel Streamlit integrado
integration/            build_snapshot.py, schema.py, decision_log.py e fontes verificadas
data/                   integrated_snapshot.json e decision_log.jsonl (gerados)
docs/                   arquitetura, matriz de integração e limitações
evidence/               evidências por módulo (logs, JSONs, gráficos extraídos)
modules/                cópias limpas dos trabalhos das disciplinas
tests/                  pytest: contrato do snapshot, log de decisão e AppTest
```

## Governança e transparência

- **Supervisão humana:** alertas exigem decisão com operador e justificativa;
  a trilha fica em `data/decision_log.jsonl` com timestamp UTC.
- **Credenciais:** uma credencial Kaggle exposta no notebook original de Visão
  foi removida da cópia de trabalho e a revogação foi solicitada ao titular.
  O segredo não está neste repositório.
- **Autoria:** a autoria do módulo de Visão Computacional está em correção
  junto ao integrante responsável.
- **Uso de IA:** IA foi utilizada como ferramenta de auditoria, integração e
  redação técnica, com revisão humana. A conclusão do relatório foi escrita
  pelos integrantes.

## Links

- Vídeo (YouTube, não listado): _[inserir URL após publicação]_
- Relatório GBA (PDF): ver entrega no portal

## Limitações principais

Nenhum modelo roda ao vivo no painel — o snapshot consolida artefatos
verificados por reexecução local ou auditoria de outputs. O módulo IoT não foi
recebido. A lista completa está em [`docs/limitations.md`](docs/limitations.md).
