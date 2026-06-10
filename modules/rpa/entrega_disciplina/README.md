# Entrega oficial da disciplina AI for RPA

Recebida em 09/06/2026 às 22h21, após o fechamento do pacote integrado.

- `GS_RPA.ipynb` — notebook Colab standalone (35 células, outputs gravados):
  gera um dataset **sintético** de 5.000 registros de meteoritos
  (`np.random.seed(42)`), classifica risco por regras de limiar de massa,
  aplica contagem de palavras-chave sobre logs gerados pelo próprio robô e
  exporta CSV, XLSX, 3 gráficos PNG e o PDF.
- `Relatorio_Space_Mission_RPA.pdf` — artefato gerado pela própria execução do
  notebook (indicadores idênticos aos outputs), com capa dos integrantes.

**Transparência:** a versão original do notebook mencionava "dados reais da
NASA", mas o código não realiza nenhuma chamada de API — todos os dados são
gerados sinteticamente em código. Em 09/06/2026 a equipe de integração
corrigiu as células de texto para alinhá-las ao código (dataset sintético no
formato NASA Open Data) e removeu um artefato de citação residual; **nenhuma
célula de código ou output foi alterado**. Os indicadores (5.000 registros;
risco Médio 2.192, Baixo 1.458, Alto 1.161, Crítico 189) descrevem esse
dataset sintético.

Este material é distinto do pipeline `modules/rpa/` (MissionOps), que foi
executado localmente pela equipe de integração e é a fonte de dados RPA do
snapshot integrado. O notebook da disciplina **não** está integrado ao painel.
