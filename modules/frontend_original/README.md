# GeoGuard IA — Global Solution Front-End 2026/1
# GeoGuard IA – Dashboard Inteligente de Monitoramento Climático

## Integrantes

 Pedro Leal Murad | RM565460 
 Ricardo de Paiva Melo | RM565522 
 Jonas Alaf | RM566479 

## Disciplina

Front-End e Mobile Development em Sistemas de IA

## Global Solution 2026/1
Dashboard interativo em Streamlit para apoio à decisão em eventos climáticos extremos usando dados satelitais/climáticos simulados.

## Problema
Gestores públicos e equipes operacionais precisam transformar sinais de clima, vegetação, focos de calor e população exposta em alertas práticos. A interface organiza essa leitura e exige validação humana antes de disparar um alerta.

## Fonte de dados
Nesta POC, os dados são mockados em `providers/climate_provider.py`, simulando variáveis satelitais e climáticas: chuva, temperatura, umidade, NDVI, vento, focos de calor e população exposta.

## Framework escolhido
Streamlit, porque permite construção rápida de dashboard, ciclo de rerun controlado com `st.session_state` e cache com `@st.cache_data`.

## Arquitetura
```text
app.py
providers/   -> geração/acesso aos dados brutos
pipelines/   -> cálculo de risco, filtros e recomendação
features/    -> tela principal do dashboard
state/       -> estado de sessão e decisões humanas
ui/          -> componentes reutilizáveis e gráficos
tests/       -> testes unitários do pipeline
```

## Requisitos atendidos
- Streamlit com `st.session_state` e `@st.cache_data`
- Arquitetura componentizada: providers, pipelines, features, state e ui
- 4 filtros interativos: data, região, categoria e threshold de risco
- 3 visualizações: 2 Plotly + 1 Matplotlib
- Tabs, sidebar, colunas, spinner e progress bar
- Cores semânticas por criticidade
- Fluxo human-in-the-loop para aprovar ou rejeitar alerta
- Testes automatizados do pipeline

## Como executar
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
streamlit run app.py
```

## Como rodar testes
```bash
pytest -q
```

## Roteiro do vídeo
1. Apresentar o problema e impacto espacial.
2. Mostrar filtros, tabs, gráficos e tabela.
3. Demonstrar loading/spinner e cache.
4. Aprovar ou rejeitar o alerta na aba Decisão humana.
5. Mostrar rapidamente a arquitetura de pastas e explicar providers, pipelines, features, state e ui.
## Autorias

Projeto desenvolvido para a Global Solution FIAP 2026/1.

Equipe:
- Pedro Leal Murad – RM565460
- Ricardo de Paiva Melo – RM565522
- Jonas Alaf – RM566479

GitHub:
https://github.com/pedrolmu/geoguard-ia-dashboard-climatico