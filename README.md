# Evasão escolar é uma escolha? (Caso IFPB-Picuí) — Pipeline SiSU 2017–2022

Este repositório contém o **pipeline reprodutível** para extrair e analisar preferências
de **curso** e **turno** no SiSU para residentes de **Picuí (PB)** (cód. IBGE **2511400**),
no período **2017–2022**.

## Fontes de dados
- Microdados do SiSU (MEC), acessados via infraestrutura pública de consulta (BigQuery) usando:
  - `basedosdados` (Python)

## Requisitos
- Python 3.10+
- Acesso ao BigQuery (com billing habilitado)
- Credenciais Google válidas

## Instalação
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt

## DOI

Este conjunto de dados está arquivado no Zenodo e possui identificador persistente (DOI):

https://doi.org/10.5281/zenodo.19006824

O DOI garante preservação, citabilidade e acesso permanente ao dataset utilizado neste estudo.

#CITAÇÃO

ABNT

SILVA, Bráulio Roberto Rangel da. Dados e pipeline de análise do SiSU
(Picuí – PB, 2017–2022). 
Zenodo, 2026. DOI: https://doi.org/10.5281/zenodo.19006824.

APA

Silva, B. R. R. (2026). Dados e pipeline de análise do SiSU 
(Picuí – PB, 2017–2022). 
Zenodo. https://doi.org/10.5281/zenodo.19006824