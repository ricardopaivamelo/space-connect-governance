# Limitações declaradas

Transparência exigida pela disciplina de Governança em IA e Business Analytics.

## Globais

- Nenhum modelo roda ao vivo no painel: o snapshot consolida artefatos
  verificados (`replayed_evidence` e `historical_notebook_output`).
- O módulo de Physical Computing/IoT não foi recebido; toda a telemetria é
  simulada ou proveniente de datasets dos demais módulos.
- As decisões humanas registradas no painel são demonstrativas, mas a trilha
  (`data/decision_log.jsonl`) é persistente e auditável.

## Por módulo

### AI for RPA
- NLP sintético com acurácia de 41,7% e recall zero para ALERTA — descartado.
- Análise de imagem é proxy de brilho/saturação, não detector semântico.
- Logs sobrescritos a cada execução; sem testes automatizados no pacote original.

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

### Front-End
- O indicador original de "população exposta" somava pessoa-dias (inflação de
  ~30,9×) e não é usado como resultado.
- Dados climáticos do protótipo original são sintéticos.
