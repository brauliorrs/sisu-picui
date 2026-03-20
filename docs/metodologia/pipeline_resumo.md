# Pipeline (resumo executivo)

## Objetivo

Reproduzir, de forma auditável, a extração e a organização de inscrições no SiSU para
residentes de Picuí (PB), com foco nas escolhas de curso e turno entre 2017 e 2022.

## Fonte de dados

- Tabela: `basedosdados.br_mec_sisu.microdados`
- Acesso: BigQuery via biblioteca `basedosdados`
- Filtro territorial: `id_municipio_candidato = '2511400'`

## Etapas

### 1. Extração (`src/01_extract_sisu.py`)

- Executa uma consulta SQL no BigQuery.
- Filtra os registros do período de 2017 a 2022.
- Restringe o universo a candidatos residentes em Picuí (PB).
- Agrega os resultados por `ano`, `nome_curso` e `turno`.
- Salva a saída em `data/raw/sisu_picui_2017_2022_agg.csv`.

### 2. Rankings e tabelas (`src/02_aggregate_rankings.py`)

- Lê o CSV agregado produzido na etapa anterior.
- Reorganiza os totais em quatro tabelas:
  - ranking agregado por curso;
  - ranking agregado por turno;
  - ranking anual por curso;
  - ranking anual por turno.
- Exporta os resultados em CSV para `data/processed/`.
- Gera um workbook consolidado em `data/processed/relatorio_picui_2017_2022.xlsx`.

### 3. Figuras (`src/03_generate_figures.py`)

- Lê os CSVs de `data/processed/`.
- Gera quatro figuras em `docs/paper/figuras/`:
  - top 15 cursos no período;
  - distribuição agregada por turno;
  - evolução anual dos turnos;
  - evolução anual de cursos selecionados do IFPB-Picuí.

### 4. Resumo de resultados (`src/04_export_report.py`)

- Lê as tabelas processadas e verifica a disponibilidade das figuras.
- Gera um resumo em Markdown em `docs/paper/resumo_resultados.md`.
- O arquivo sintetiza tabelas e observações metodológicas para apoiar a escrita do artigo.

## Interpretação dos dados

As contagens são inscrições no SiSU. Elas não devem ser lidas automaticamente como
matrículas, permanência ou evasão. O pipeline organiza preferências declaradas em
inscrições, cabendo ao artigo fazer a articulação teórica dessas evidências.
