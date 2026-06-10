# Análise detalhada - Computação Neuromórfica

## 1. Veredito

O trabalho **atende ao formato de protótipo conceitual** solicitado pela
disciplina. Ele usa memória memristiva virtual, limiar de disparo e
processamento orientado a eventos em um cenário de rover lunar.

O material precisa de correções antes da integração. Há uma inconsistência
numérica crítica entre notebook e PDF. O dataset, ausente do ZIP original, foi
recebido em 09/06/2026 e permitiu reexecutar a lógica localmente. A comparação
com os rótulos reais mostrou que a recomendação do Ajuste B não é sustentada
pelas métricas: o Ajuste A tem acurácia maior e detecta as transições com menos
atraso.

## 2. Atendimento ao enunciado

| Requisito | Evidência | Avaliação |
|---|---|---|
| Cenário espacial ou espaço-Terra | Rover lunar autônomo | Atendido |
| Condição crítica | Temperatura, radiação e poeira | Atendido |
| Sensor neuromórfico conceitual | Estado acumulado chamado memristor virtual | Atendido |
| Baixo consumo | Proposta de transmissão somente por eventos | Conceitualmente atendido, não medido |
| Conceito estudado no semestre | Memristor, limiar e processamento por eventos | Atendido |
| Teste do protótipo | Comparação de três perfis | Atendido com limitações |

## 3. Materiais recebidos

Entrega original (`GS_CN/`):

- `GS_CN.ipynb`;
- `relatorio_global_solution_2026_final.pdf`.

Recebidos posteriormente em `fontes_fornecidas/` (09/06/2026):

- `dataset_neurosensor_espacial_5h.csv` (61 registros, 0 a 300 minutos);
- `Colab_NeuroSpace_Alert.ipynb` (notebook-base oficial da disciplina);
- `Atividade_Global_Solution_NeuroSpace_Alert.docx` (enunciado da atividade).

Continuam ausentes:

- `saida_sensor_espacial_Ajuste_B_equilibrado_grupo.csv` (saída original do
  grupo; foi regenerada localmente como evidência);
- arquivo de dependências;
- script executável fora do Google Colab (a reexecução local exigiu adaptação).

O notebook contém 28 células, sendo 16 de código, com outputs gravados e sem
erros registrados na execução original.

## 4. Funcionamento observado

### Dataset descrito

O notebook registra:

- 61 leituras;
- intervalo de 0 a 300 minutos;
- uma leitura a cada 5 minutos;
- temperatura;
- radiação;
- poeira;
- consumo;
- bateria;
- índice de risco real;
- condição real.

### Sinal conceitual

As variáveis são normalizadas com mínimo e máximo do dataset inteiro:

```text
V_entrada = 12
          + temperatura_normalizada * 10
          + radiacao_normalizada * 14
          + poeira_normalizada * 10
```

Os outputs gravados informam:

- `V_entrada` mínimo: 12,0;
- `V_entrada` máximo: aproximadamente 45,61.

### Memristor virtual

Para cada leitura:

- se `V_entrada > V_limiar`, o estado aumenta pelo excesso multiplicado pela
  taxa de chaveamento;
- caso contrário, o estado é multiplicado por 0,995;
- o estado é limitado entre 0 e 1;
- abaixo de 0,35: `NORMAL`;
- entre 0,35 e 0,70: `OBSERVACAO`;
- a partir de 0,70: `ALERTA_CRITICO`.

### Perfis do notebook

| Perfil | V_limiar | Taxa |
|---|---:|---:|
| A - Sensível | 25 | 0,0065 |
| B - Equilibrado | 29 | 0,0055 |
| C - Conservador | 33 | 0,0040 |

### Resultados gravados

| Perfil | Sai do apagado | Fica vermelho |
|---|---:|---:|
| A - Sensível | 190 min | 215 min |
| B - Equilibrado | 215 min | 240 min |
| C - Conservador | 250 min | 290 min |

## 5. Reprodução e testes

### Reexecução integral

A primeira tentativa de reexecução foi bloqueada porque o dataset não estava no
ZIP e o notebook depende de `google.colab.files.upload`.

Após o recebimento de `dataset_neurosensor_espacial_5h.csv`, a lógica dos dois
notebooks (base oficial e entrega do grupo) foi reexecutada localmente, com a
dependência de upload substituída por leitura direta do arquivo.

Dataset confirmado:

- 61 registros, de 0 a 300 minutos, um a cada 5 minutos;
- `condicao_real`: 31 `NORMAL`; 9 `ATENCAO`, de 155 a 195 min; 21 `CRITICA`,
  de 200 a 300 min.

#### Comparação notebook-base oficial x entrega do grupo

Notebook-base oficial (sinal `V_entrada` entre 16,01 e 37,17):

| Ajuste | Limiar / Taxa | Amarelo (min) | Vermelho (min) | Acurácia vs `condicao_real` |
|---|---|---:|---:|---:|
| A | 24 / 0,006 | 170 | 190 | 91,80% |
| B | 28 / 0,005 | 205 | 225 | 77,05% |
| C | 32 / 0,004 | 245 | 280 | 59,02% |

Notebook entregue pelo grupo (fórmula de entrada alterada; sinal entre 12,0 e
45,61):

| Ajuste | Limiar / Taxa | Amarelo (min) | Vermelho (min) | Acurácia vs `condicao_real` |
|---|---|---:|---:|---:|
| A | 25 / 0,0065 | 190 | 215 | 83,61% |
| B | 29 / 0,0055 | 215 | 240 | 72,13% |
| C | 33 / 0,0040 | 250 | 290 | 55,74% |

Observações da comparação:

- o grupo alterou a fórmula de entrada e a dinâmica do sensor em relação ao
  notebook-base oficial, o que desloca todas as transições;
- a `ATENCAO` real começa aos 155 min e a `CRITICA` aos 200 min; o Ajuste B
  recomendado pelo grupo acende o amarelo 60 minutos após o início de
  `ATENCAO` e o vermelho 40 minutos após o início de `CRITICA`;
- o Ajuste A entregue reage mais rápido: 35 minutos para o amarelo e 15 para o
  vermelho, com acurácia maior (83,61% contra 72,13%);
- a disciplina pedia comparação das transições entre perfis, não maximização de
  acurácia; ainda assim, a recomendação do Ajuste B precisa justificar o atraso
  adicional de detecção;
- evidências em `03_integracao/evidencias/computacao_neuromorfica/`:
  `comparacao_base_vs_entrega.csv`, `comparacao_base_vs_entrega.json` e
  `saida_sensor_espacial_Ajuste_B_entrega.csv`.

### Execução da função central

A função `simular_sensor` foi extraída diretamente do notebook e executada
localmente.

Usando continuamente o maior `V_entrada` registrado, 45,61:

| Limiar | Estado final | Resultado |
|---:|---:|---|
| 25 | 1,0 | Dispara |
| 29 | 1,0 | Dispara |
| 33 | 1,0 | Dispara |
| 250 | 0,0 | Nunca dispara |
| 290 | 0,0 | Nunca dispara |
| 330 | 0,0 | Nunca dispara |

Esse teste confirma que os resultados do notebook dependem dos limiares
`25/29/33`.

## 6. Problemas encontrados

### Alta - relatório apresenta limiares dez vezes maiores

O PDF informa:

- 250;
- 290;
- 330.

O notebook executado usa:

- 25;
- 29;
- 33.

Como o maior sinal registrado é 45,61, os valores do PDF impossibilitam qualquer
transição. O PDF precisa ser corrigido antes de ser usado no relatório
integrador.

### Resolvida em parte - arquivos chegaram depois da entrega original

O ZIP original não continha o dataset. Ele foi recebido em 09/06/2026 em
`fontes_fornecidas/`, o que permitiu:

- confirmar os 61 registros e os rótulos;
- validar as transições dos dois notebooks;
- comparar o sensor com `condicao_real`;
- regenerar a saída do Ajuste B (`saida_sensor_espacial_Ajuste_B_entrega.csv`).

Permanece o problema de origem: o pacote entregue à disciplina não é
autossuficiente, pois quem receber apenas o ZIP não consegue reexecutar.
O dataset deve entrar no repositório consolidado.

### Alta - rótulos reais existem, mas não são usados na avaliação

O dataset possui:

- `indice_risco_real`;
- `condicao_real`.

O notebook não compara os eventos produzidos com essas colunas. Portanto, não
calcula:

- acurácia;
- precisão;
- recall;
- falsos positivos;
- falsos negativos;
- atraso em relação ao início da condição crítica.

Sem essa comparação, não havia evidência de que o Ajuste B fosse o melhor. Ele
foi escolhido por posição intermediária, não por métrica de desempenho. A
comparação realizada nesta auditoria (seção 5) confirmou que, contra
`condicao_real`, o Ajuste A supera o B nos dois notebooks (83,61% contra 72,13%
na entrega; 91,80% contra 77,05% no base) e detecta as transições com menos
atraso.

### Alta - normalização usa conhecimento do futuro

O mínimo e o máximo são calculados sobre as cinco horas completas. Um sensor
embarcado em operação não conhece antecipadamente o maior e o menor valor que
serão observados.

Para uma simulação offline isso funciona, mas para representar edge computing
os limites devem ser:

- definidos por especificação do sensor;
- calibrados previamente;
- ou atualizados por uma janela histórica controlada.

### Média - comportamento depende da frequência de amostragem

A atualização do memristor não usa `tempo_min` nem um `delta_t`. Ela acontece
uma vez por linha.

Em um teste com o mesmo sinal de entrada durante 50 minutos:

| Intervalo de amostragem | Leituras | Estado final | LED |
|---:|---:|---:|---|
| 5 minutos | 11 | 0,6655 | AMARELO |
| 1 minuto | 51 | 1,0 | VERMELHO |

O mesmo fenômeno físico gera decisões diferentes apenas pela taxa de coleta.
A equação deve incorporar o tempo transcorrido.

### Média - economia de energia não foi medida

O relatório afirma redução importante de transmissão e consumo, mas não
calcula:

- quantidade de mensagens evitadas;
- energia por transmissão;
- consumo antes e depois;
- autonomia estimada.

Além disso, a saída atual registra um evento em todas as 61 linhas. Para
materializar a proposta, o sistema deveria emitir apenas transições de estado,
alertas e heartbeats programados.

Como referência, duas transições em vez de 61 transmissões representariam
redução potencial de aproximadamente 96,7%, mas esse valor ainda não foi medido
no projeto.

### Média - parâmetros sem justificativa técnica

Não foi apresentada calibração para:

- pesos 10, 14 e 10;
- valor base 12;
- limiares 25, 29 e 33;
- taxas de chaveamento;
- decaimento 0,995;
- limites 0,35 e 0,70.

Eles podem ser usados em uma POC, mas devem ser identificados como parâmetros
experimentais.

### Média - memristor é uma abstração algorítmica

O código representa uma variável acumuladora limitada entre 0 e 1. Ele não
modela tensão, corrente, resistência, histerese ou uma equação física de
memristor.

Isso não invalida o protótipo conceitual, mas o relatório deve evitar afirmar
que validou um dispositivo físico.

### Média - afirmação de fatores simultâneos é imprecisa

O sinal é uma soma ponderada. Dependendo do perfil, uma variável muito alta pode
contribuir mais que as demais e iniciar o acúmulo. O código não exige
explicitamente que temperatura, radiação e poeira estejam simultaneamente em
faixas críticas.

## 7. Pontos fortes

- cenário claro e compatível com o tema espacial;
- uso de três conceitos da disciplina;
- código curto e fácil de explicar;
- comparação visual entre perfis;
- outputs gravados sem erros;
- estado acumulado representa memória temporal;
- resultado adequado a uma demonstração;
- saída tabular pode ser integrada ao RPA;
- baixo custo computacional.

## 8. Correções obrigatórias

1. Corrigir o PDF para `25`, `29` e `33`.
2. Incluir o dataset original.
3. Incluir a saída CSV do Ajuste B.
4. Remover a dependência obrigatória de upload do Colab.
5. Adicionar execução local com caminho de arquivo.
6. Comparar eventos com `condicao_real`.
7. Calcular métricas por ajuste.
8. Escolher o perfil recomendado com base nessas métricas.
9. Incorporar `delta_t` à atualização do estado.
10. Quantificar mensagens e economia potencial.

## 9. Integração recomendada

### Posição no fluxo

```text
Physical Computing/IoT, se recebido
  -> temperatura, radiação e poeira
  -> sensor neuromórfico
  -> somente eventos relevantes
  -> RPA integrador
  -> dashboard e decisão humana
```

### Saída mínima para o RPA

Cada transição deve conter:

- timestamp;
- perfil do sensor;
- temperatura;
- radiação;
- poeira;
- `V_entrada`;
- estado do memristor;
- estado anterior;
- novo estado;
- evento;
- motivo;
- versão dos parâmetros.

### Uso no vídeo

O gráfico de transições é uma evidência visual útil. A apresentação deve dizer
que se trata de uma simulação conceitual e que o módulo reduz o tráfego ao
transformar leituras contínuas em eventos, sem alegar economia energética
medida.

## 10. Decisão

**Integrar como evidência reexecutada e verificada.**

O dataset chegou e a reexecução local confirmou as transições do notebook
entregue. O módulo entra na integração como `replayed_evidence`, com as
ressalvas documentadas: limiares do PDF divergentes do código (250/290/330
contra 25/29/33), dependência da frequência de amostragem pela ausência de
`delta_t`, economia de energia não medida e recomendação do Ajuste B não
sustentada pela comparação com os rótulos reais.

## 11. Evidências preservadas

Foram extraídos quatro gráficos do notebook para:

`03_integracao/evidencias/computacao_neuromorfica/`

Os gráficos mostram:

- evolução das variáveis;
- evolução de `V_entrada`;
- estado do memristor;
- transições do LED.

A reexecução local com o dataset recebido acrescentou:

- `comparacao_base_vs_entrega.csv`;
- `comparacao_base_vs_entrega.json`;
- `saida_sensor_espacial_Ajuste_B_entrega.csv`.
