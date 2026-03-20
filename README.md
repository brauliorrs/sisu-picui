# Evasão escolar e mobilidade territorial? Caso IFPB-Picuí no SiSU (2017-2022)

Este repositório reúne o pipeline de dados e a documentação técnica usados para analisar
as escolhas de curso e turno no Sistema de Seleção Unificada (SiSU) entre residentes de
Picuí (PB), código IBGE `2511400`, no período de 2017 a 2022.

O estudo dialoga com a hipótese de não adesão territorial como alternativa interpretativa
ao uso automático da noção de evasão. O foco empírico aqui não é medir permanência ou
abandono, mas mapear preferências declaradas de inscrição no SiSU e sua distribuição
temporal.

## Estrutura do repositório

```text
data/
  raw/        saídas intermediárias da extração
  processed/  rankings, tabelas consolidadas e planilhas finais
docs/
  metodologia/  notas técnicas do pipeline
  paper/        figuras e resumos usados na redação do artigo
src/            scripts do pipeline reprodutível
dashboard/      painel Streamlit para leitura interativa dos resultados
ranking_picui.py  ponto de entrada para rodar o pipeline completo
```

## Fonte dos dados

- Base pública: `basedosdados.br_mec_sisu.microdados`
- Acesso: BigQuery, via biblioteca Python `basedosdados`
- Recorte: residentes em Picuí (PB)
- Janela temporal: 2017-2022

## Unidade analítica

As contagens representam inscrições registradas no SiSU. Elas não equivalem, por si só,
a matrículas, permanência, conclusão ou evasão. Essa distinção precisa ser mantida no
texto do artigo e nas legendas das tabelas e figuras.

## Como executar

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

Execute as etapas na ordem abaixo:

```bash
python src/01_extract_sisu.py --billing-project SEU_PROJETO_GCP
python src/02_aggregate_rankings.py
python src/03_generate_figures.py
python src/04_export_report.py
```

Se preferir usar o ponto de entrada legado:

```bash
python ranking_picui.py --billing-project SEU_PROJETO_GCP
```

## Painel em Streamlit

Para abrir o painel interativo de leitura dos resultados:

```bash
streamlit run dashboard/app.py
```

O app consome os arquivos já gerados em `data/processed/` e o resumo em
`docs/paper/resumo_resultados.md`. As figuras estáticas permanecem como saídas do pipeline
para uso no artigo escrito e em material suplementar.

## Produtos gerados

- `data/raw/sisu_picui_2017_2022_agg.csv`: extração agregada por ano, curso e turno
- `data/processed/ranking_cursos_picui_2017_2022.csv`: total de inscrições por curso
- `data/processed/ranking_turnos_picui_2017_2022.csv`: total de inscrições por turno
- `data/processed/ranking_cursos_por_ano_picui_2017_2022.csv`: série anual por curso
- `data/processed/ranking_turnos_por_ano_picui_2017_2022.csv`: série anual por turno
- `data/processed/relatorio_picui_2017_2022.xlsx`: planilha consolidada
- `docs/paper/resumo_resultados.md`: resumo técnico em Markdown
- `docs/paper/figuras/*.png`: figuras para o artigo
- `dashboard/app.py`: painel Streamlit para leitura interativa

## DOI

Este conjunto de dados e pipeline está arquivado no Zenodo e possui identificador persistente:

[https://doi.org/10.5281/zenodo.19006824](https://doi.org/10.5281/zenodo.19006824)

O DOI garante preservação, citabilidade e acesso permanente ao material utilizado no estudo.

## Como citar

Os metadados formais do repositório estão em [CITATION.cff](/D:/sisu_picui/CITATION.cff).

Referência sugerida em ABNT:

SILVA, Bráulio Roberto Rangel da. *Dados e pipeline de análise do SiSU (Picuí – PB, 2017–2022).* Zenodo, 2026. DOI: https://doi.org/10.5281/zenodo.19006824.

Referência sugerida em APA:

Silva, B. R. R. (2026). *Dados e pipeline de análise do SiSU (Picuí – PB, 2017–2022).* Zenodo. https://doi.org/10.5281/zenodo.19006824

## Documentação metodológica

- [pipeline_resumo.md](/D:/sisu_picui/docs/metodologia/pipeline_resumo.md)
- [dicionario_variaveis.md](/D:/sisu_picui/docs/metodologia/dicionario_variaveis.md)

## Reprodutibilidade

Os arquivos de `data/raw/` e `data/processed/` podem ser regenerados pelos scripts.
Como parte do fluxo normal de pesquisa, o repositório versiona a estrutura e a
documentação, mas evita manter saídas volumosas ou redundantes no Git.
