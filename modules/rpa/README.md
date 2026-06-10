# 🛰️ MissionOps RPA — Robô de Triagem e Análise Multimodal de Dados de Missão

Projeto **Global Solution 2026 — AI for RPA (Robotic Process Automation)** · FIAP.

Um "robô" (pipeline automatizado de ponta a ponta) inspirado nos desafios da
**exploração espacial**. Ele varre uma pasta de entrada com dados brutos e não
estruturados de missão — **telemetria, logs/relatórios e imagens de sensores** —
e os transforma automaticamente em **inteligência acionável**: detecta
anomalias, classifica severidade, extrai entidades e gera artefatos técnicos
(planilha, relatório PDF e dados para um dashboard).

## 🎯 Como o projeto atende aos critérios da avaliação

| Critério (peso) | Como é atendido |
|---|---|
| **Domínio técnico + integração de ≥2 tópicos (40%)** | Combina **RPA** (automação do fluxo de arquivos e geração de artefatos) com **IA** em três frentes: detecção de anomalias (ML), NLP e visão computacional. |
| **Arquitetura de fluxo + engenharia (25%)** | Pipeline modular em etapas, **tratamento de exceção por item** (uma falha não derruba o lote), logging completo da execução. |
| **Inteligência de dados + recursos de IA (20%)** | Isolation Forest + z-score (telemetria); classificador TF-IDF + Regressão Logística e extração de entidades (documentos); visão computacional clássica (imagens). |
| **Entrega de artefatos + outputs (15%)** | Planilha Excel estruturada (abas + fórmulas), relatório PDF consolidado e JSON estruturado consumido por um **dashboard** front-end. |

## 🧱 Arquitetura do fluxo

```
        inbox/  (telemetria .csv | logs .txt/.log/.pdf | imagens .png/.jpg)
              |
              v
   [1] LOADER  -> varre, classifica por tipo e valida cada arquivo
              |
              v
   [2] PROCESSADORES (IA)  -> cada arquivo em try/except (resiliência)
        |-- Telemetria : Isolation Forest + z-score  (anomalias)
        |-- Documentos : NLP (classificador ML + extração de entidades)
        |-- Imagens    : Visão Computacional (hotspots, brilho, nitidez)
              |
              v
   [3] CONSOLIDAÇÃO  -> estatísticas e relatório de execução
              |
              v
   [4] ARTEFATOS  -> Excel + PDF + JSON
              |
              v
   [5] DASHBOARD (Streamlit) carrega o JSON estruturado
              |
        logs/execucao.log  (registro completo, sucessos e falhas)
```

## 🧰 Tecnologias

Python · pandas · NumPy · scikit-learn (Isolation Forest, TF-IDF, Regressão
Logística) · Pillow (visão computacional) · openpyxl (Excel) · reportlab (PDF)
· pypdf (leitura de PDF) · Streamlit (dashboard).

## ⚙️ Instalação

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ Como executar

```bash
# 1. rodar o robô (a pasta inbox/ já vem com dados de amostra prontos)
python run.py

# 2. abrir o dashboard com os resultados
streamlit run dashboard.py
```

> A pasta `inbox/` já vem com 9 arquivos de amostra prontos: 2 telemetrias
> (CSV), 3 logs/relatórios e 3 imagens de sensor. Para usar seus próprios
> dados, é só substituir os arquivos da pasta.
>
> **Crédito das imagens:** as imagens de sensor são da NASA (domínio público) —
> IDs originais `GSFC_20171208_Archive_e000963` (Sol/SDO), `PIA08189`
> (lua Tethys/Cassini) e `PIA12066` (campo de estrelas). Fonte: images.nasa.gov.

Para usar **seus próprios dados**, basta colocar os arquivos na pasta `inbox/`
(CSV de telemetria, TXT/LOG/PDF de relatórios, PNG/JPG de imagens) e rodar
`python run.py`.

## 📦 Artefatos gerados (em `outputs/`)

- **`relatorio_missao.xlsx`** — planilha com abas Resumo (com fórmulas),
  Telemetria, Documentos e Imagens, com severidade destacada por cor.
- **`relatorio_missao.pdf`** — relatório consolidado: indicadores, itens
  críticos e falhas de processamento.
- **`resultado.json`** — dados estruturados consumidos pelo dashboard.

## 📁 Estrutura

```
missionops-rpa/
├── run.py                     # ponto de entrada do robô
├── dashboard.py               # front-end (Streamlit)
├── requirements.txt
├── README.md
├── robo/
│   ├── config.py              # parâmetros centrais
│   ├── logger.py              # logging em arquivo + console
│   ├── loader.py              # etapa 1: varredura e classificação
│   ├── pipeline.py            # orquestrador com error handling
│   ├── artefatos.py           # geração de Excel, PDF e JSON
│   └── processadores/
│       ├── telemetria.py      # anomalias (Isolation Forest + z-score)
│       ├── documentos.py      # NLP (classificação + entidades)
│       └── imagens.py         # visão computacional
├── inbox/                     # entrada (dados brutos)
├── outputs/                   # artefatos gerados
└── logs/                      # log de execução
```

## ⚠️ Limitações

- A classificação de severidade de documentos usa um classificador treinado em
  exemplos sintéticos (PT/EN); um corpus rotulado real aumentaria a precisão.
- A visão computacional é clássica (sem modelo de deep learning), focada em
  brilho/hotspots/nitidez — adequada à demonstração, mas não classifica o
  conteúdo semântico da imagem.
- PDFs escaneados (imagem) não têm texto extraível sem OCR.

## 🚀 Melhorias futuras

- Monitoramento contínuo da pasta (watcher) para processamento em tempo real.
- Modelos de deep learning para classificação semântica de imagens.
- Fila de mensagens para escalar o processamento em paralelo.
- Notificações automáticas (e-mail/Slack) ao detectar itens críticos.
- Persistência em banco de dados e histórico de execuções.
```
