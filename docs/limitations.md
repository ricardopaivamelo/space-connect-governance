# Limitações declaradas

Transparência exigida pela disciplina de Governança em IA e Business Analytics.

## Globais

- Nenhum modelo roda ao vivo no painel: o snapshot consolida artefatos
  verificados (`replayed_evidence` e `historical_notebook_output`).
- O módulo de Physical Computing/IoT (AgroSat Monitor) foi recebido apenas às
  22h23 de 09/06/2026, após o fechamento do pacote integrado: o código foi
  auditado (ESP32 simulado no Wokwi, MQTT, Node-RED, InfluxDB, Grafana), mas
  não há evidência de execução e a integração técnica não foi realizada. Toda
  a telemetria da plataforma segue simulada ou proveniente de datasets dos
  demais módulos.
- As decisões humanas registradas no painel são demonstrativas, mas a trilha
  (`data/decision_log.jsonl`) é persistente e auditável.

## Por módulo

### AI for RPA
- NLP sintético com acurácia de 41,7% e recall zero para ALERTA — descartado.
- Análise de imagem é proxy de brilho/saturação, não detector semântico.
- Logs sobrescritos a cada execução; sem testes automatizados no pacote original.
- A entrega oficial da disciplina (notebook GS_RPA, recebido às 22h21 de
  09/06) é um artefato standalone com dataset sintético de 5.000 registros
  gerado em código — o texto menciona "dados da NASA", mas não há chamadas de
  API; ver `modules/rpa/entrega_disciplina/README.md`.

### Computação Neuromórfica
- PDF do grupo cita limiares 250/290/330; o código usa 25/29/33.
- A dinâmica não usa `delta_t`: o resultado depende da frequência de amostragem.
- Economia de energia é proposta, não medida.
- A recomendação do Ajuste B não é sustentada pela comparação com
  `condicao_real` (o Ajuste A tem acurácia maior e menos atraso).

### Computação Quântica e IA
- Sem vantagem quântica: QSVC médio (60,95%) abaixo do SVM (74,29%) e do
  baseline majoritário (61,90%).
- Execução simulada, sem hardware quântico e sem modelo de ruído.

### Visão Computacional
- Métricas reais do notebook: 98,02% de acurácia (o PDF declara 99,4%, valor
  não correspondente aos outputs).
- 32 das 6.300 imagens não entraram na avaliação.
- Dataset canadense; sem teste geográfico externo; não prova detecção de
  incêndio ativo nem generalização para o Brasil.
- Dataset e modelo treinado não foram entregues; autoria em correção.

### PLN, Chatbots e Virtual Agents
- Implementa somente recuperação semântica (31 chunks, FAISS, top-k).
- Sem LLM, geração, prompt, interface ou comparação RAG × LLM puro.
- Os valores "Llama 3.2 3B" e "90% de assertividade" do relatório original não
  têm evidência no notebook e não são repetidos nesta entrega.
- O corpus original de dez PDFs (edificações sustentáveis: LEED, AQUA-HQE,
  PROCEL etc.) segue ausente; quatro PDFs alternativos de tema espacial
  recebidos às 22h20 de 09/06 não foram indexados por nenhum pipeline — ver
  `evidence/rag/corpus_manifest.md`.

### Front-End
- O indicador original de "população exposta" somava pessoa-dias (inflação de
  ~30,9×) e não é usado como resultado.
- Dados climáticos do protótipo original são sintéticos.
