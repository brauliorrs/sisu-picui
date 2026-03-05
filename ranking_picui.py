# ranking_picui_2017_2022_cursos_turnos.py
# Gera rankings de CURSOS e TURNOS para Picuí (PB) no SiSU, de 2017 a 2022.
# Saídas:
# - ranking_cursos_picui_2017_2022.csv / .xlsx
# - ranking_turnos_picui_2017_2022.csv / .xlsx
# - ranking_cursos_por_ano_picui_2017_2022.csv / .xlsx
# - ranking_turnos_por_ano_picui_2017_2022.csv / .xlsx
# - Um Excel consolidado: relatorio_picui_2017_2022.xlsx (4 abas)

import os
import basedosdados as bd

# =========================
# CONFIG
# =========================
BILLING_ID = "sisu-picui"     # <-- TROQUE pelo seu Project ID (Google Cloud)
MUNICIPIO_ID = "2511400"      # Picuí (como aparece na base)
ANO_INI = 2017
ANO_FIM = 2022

TABLE = "basedosdados.br_mec_sisu.microdados"

# =========================
# QUERIES
# =========================
QUERY_CURSOS_TOTAL = f"""
SELECT
  nome_curso AS curso,
  COUNT(*) AS total_inscricoes
FROM `{TABLE}`
WHERE id_municipio_candidato = "{MUNICIPIO_ID}"
  AND ano BETWEEN {ANO_INI} AND {ANO_FIM}
GROUP BY curso
ORDER BY total_inscricoes DESC
"""

QUERY_TURNOS_TOTAL = f"""
SELECT
  turno,
  COUNT(*) AS total_inscricoes
FROM `{TABLE}`
WHERE id_municipio_candidato = "{MUNICIPIO_ID}"
  AND ano BETWEEN {ANO_INI} AND {ANO_FIM}
GROUP BY turno
ORDER BY total_inscricoes DESC
"""

QUERY_CURSOS_POR_ANO = f"""
SELECT
  ano,
  nome_curso AS curso,
  COUNT(*) AS total_inscricoes
FROM `{TABLE}`
WHERE id_municipio_candidato = "{MUNICIPIO_ID}"
  AND ano BETWEEN {ANO_INI} AND {ANO_FIM}
GROUP BY ano, curso
ORDER BY ano, total_inscricoes DESC
"""

QUERY_TURNOS_POR_ANO = f"""
SELECT
  ano,
  turno,
  COUNT(*) AS total_inscricoes
FROM `{TABLE}`
WHERE id_municipio_candidato = "{MUNICIPIO_ID}"
  AND ano BETWEEN {ANO_INI} AND {ANO_FIM}
GROUP BY ano, turno
ORDER BY ano, total_inscricoes DESC
"""

# =========================
# EXEC
# =========================
def run_query(query: str):
    return bd.read_sql(query=query, billing_project_id=BILLING_ID)

def save_csv_xlsx(df, base_name: str):
    csv_path = f"{base_name}.csv"
    xlsx_path = f"{base_name}.xlsx"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    df.to_excel(xlsx_path, index=False)
    print("Arquivos gerados:")
    print(" -", os.path.abspath(csv_path))
    print(" -", os.path.abspath(xlsx_path))

def main():
    periodo = f"{ANO_INI}_{ANO_FIM}"

    print(f"\n=== Ranking de CURSOS — Picuí ({MUNICIPIO_ID}) — SiSU {ANO_INI}-{ANO_FIM} ===")
    df_cursos_total = run_query(QUERY_CURSOS_TOTAL)
    print(df_cursos_total.head(60).to_string(index=False))
    if len(df_cursos_total) > 60:
        print(f"\n... ({len(df_cursos_total)} cursos no total; mostrando 60 primeiros)")
    save_csv_xlsx(df_cursos_total, f"ranking_cursos_picui_{periodo}")

    print(f"\n=== Ranking de TURNOS — Picuí ({MUNICIPIO_ID}) — SiSU {ANO_INI}-{ANO_FIM} ===")
    df_turnos_total = run_query(QUERY_TURNOS_TOTAL)
    print(df_turnos_total.to_string(index=False))
    save_csv_xlsx(df_turnos_total, f"ranking_turnos_picui_{periodo}")

    print(f"\n=== Ranking de CURSOS por ANO — Picuí ({MUNICIPIO_ID}) — SiSU {ANO_INI}-{ANO_FIM} ===")
    df_cursos_ano = run_query(QUERY_CURSOS_POR_ANO)
    print(df_cursos_ano.head(60).to_string(index=False))
    if len(df_cursos_ano) > 60:
        print(f"\n... ({len(df_cursos_ano)} linhas no total; mostrando 60 primeiras)")
    save_csv_xlsx(df_cursos_ano, f"ranking_cursos_por_ano_picui_{periodo}")

    print(f"\n=== Ranking de TURNOS por ANO — Picuí ({MUNICIPIO_ID}) — SiSU {ANO_INI}-{ANO_FIM} ===")
    df_turnos_ano = run_query(QUERY_TURNOS_POR_ANO)
    print(df_turnos_ano.to_string(index=False))
    save_csv_xlsx(df_turnos_ano, f"ranking_turnos_por_ano_picui_{periodo}")

    # Excel consolidado (4 abas)
    consolidated_path = f"relatorio_picui_{periodo}.xlsx"
    with __import__("pandas").ExcelWriter(consolidated_path, engine="openpyxl") as writer:
        df_cursos_total.to_excel(writer, sheet_name="cursos_total", index=False)
        df_turnos_total.to_excel(writer, sheet_name="turnos_total", index=False)
        df_cursos_ano.to_excel(writer, sheet_name="cursos_por_ano", index=False)
        df_turnos_ano.to_excel(writer, sheet_name="turnos_por_ano", index=False)

    print("\nExcel consolidado gerado:")
    print(" -", os.path.abspath(consolidated_path))

if __name__ == "__main__":
    main()