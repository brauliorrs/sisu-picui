# Pipeline (resumo executivo)

## Objetivo
Reproduzir, de forma auditável, a extração e análise de escolhas de curso e turno no SiSU
para residentes de Picuí (PB), no período 2017–2022.

## Fonte de dados
- Microdados do SiSU, via infraestrutura pública de consulta (BigQuery) acessada por:
  - `basedosdados` (Python)

## Etapas

### (1) Extração (src/01_extract_sisu.py)
- Consulta SQL no dataset `basedosdados.br_mec_sisu.microdados`
- Filtra:
  - `ano` entre 2017 e 2022
  - `id_municipio_candidato` igual ao código IBGE do município (Picuí = 2511400)
- Agrega no BigQuery:
  - por `ano`, `nome_curso`, `turno`
- Salva CSV em `data/raw/sisu_picui_2017_2022_agg.csv`

### (2) Rankings e tabelas (src/02_aggregate_rankings.py)
- A partir do CSV agregado:
  - Ranking agregado por cursos (2017–2022)
  - Ranking agregado por turnos (2017–2022)
  - Ranking por ano (cursos e turnos)
- Exporta:
  - CSVs em `data/processed/`
  - XLSX consolidado em `data/processed/relatorio_picui_2017_2022.xlsx`

### (3) Figuras (src/03_generate_figures.py)
Gera PNGs em `docs/paper/figuras/`:
- Top 15 cursos agregados
- Turnos agregados (2017–2022)
- Turnos por ano (2017–2022)
- Cursos do IFPB-Picuí por ano (subset)

### (4) “Pacote de resultados” (src/04_export_report.py)
- Gera um resumo em Markdown com tabelas principais e caminhos das figuras,
  pronto para colar no artigo.