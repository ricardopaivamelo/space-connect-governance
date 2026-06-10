# Manifesto do corpus — módulo PLN/RAG

## Corpus original (indexado pelo notebook) — NÃO fornecido

O notebook `GS_PLN_CB_&_VA.ipynb` indexou, via upload manual no Colab, dez
PDFs sobre **edificações sustentáveis** (01_LEED, 02_AQUA_HQE, 03_Net_Zero,
04_Energia_Fotovoltaica, 05_Reuso_Agua, 06_Aguas_Cinzas, ..., 10_PROCEL).
Nenhum desses dez arquivos foi entregue à equipe de integração — os 31 chunks
auditados não podem ser reproduzidos. Nota-se também a divergência temática
com o cenário espacial da Global Solution.

## Corpus alternativo recebido tardiamente (09/06/2026 22h20) — NÃO indexado

Quatro PDFs de tema espacial/climático foram recebidos após o fechamento do
pacote integrado. Eles **não** pertencem ao corpus original e **não** passaram
por nenhum pipeline; ficam registrados como material de referência para uma
futura implementação do RAG.

| Arquivo | Natureza | Páginas | SHA256 |
|---|---|---|---|
| `queimadas_inpe.pdf` (incluído aqui) | resumo sintético gerado em Python/ReportLab em 08/06/2026 | 1 | `414b50670f9530613a9f25f3a6b2abfc9f99bed354d7ef8875f05787358e60de` |
| `nasa_climate.pdf` (incluído aqui) | resumo sintético gerado em Python/ReportLab em 08/06/2026 | 1 | `0fc451cbe0fddd3d0d2c884b9477cac389ea052b3df753919a55e1065cbc0be3` |
| CEOS Earth Observation Handbook 2023 — *Space Data for the Global Stocktake* | documento público real (CEOS, 2023) — não commitado (11 MB); disponível em ceos.org/eohandbook | 117 | `41dbd7b9200040dc2375e0dced2dd936c1d832837ecb24d5ad85355c3b6b98ae` |
| *Advancing NASA's Climate Strategy* (NASA, 2023) | documento público real — não commitado (27 MB); disponível em nasa.gov | 32 | `f71b5a3e758f292fe06197bbe3b499fa0dfba915e44bc06f5e9a775af12638f5` |

Os dois resumos sintéticos estão incluídos neste diretório por serem leves
(5,5 KB) e estarem claramente rotulados como gerados por código. Os dois
documentos públicos grandes (~38 MB) são apenas referenciados, para manter o
repositório leve; os hashes acima permitem verificar a integridade das cópias
locais.
