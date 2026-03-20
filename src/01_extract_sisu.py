import argparse
from pathlib import Path

import basedosdados as bd


def build_query(ano_ini: int, ano_fim: int, municipio: str) -> str:
    municipio = municipio.strip()
    return f"""
    SELECT
      ano,
      nome_curso,
      turno,
      COUNT(1) AS total_inscricoes
    FROM `basedosdados.br_mec_sisu.microdados`
    WHERE ano BETWEEN {ano_ini} AND {ano_fim}
      AND id_municipio_candidato = '{municipio}'
    GROUP BY ano, nome_curso, turno
    ORDER BY ano, total_inscricoes DESC
    """


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--billing-project", required=True, help="Projeto de billing do BigQuery")
    ap.add_argument("--ano-ini", type=int, default=2017)
    ap.add_argument("--ano-fim", type=int, default=2022)
    ap.add_argument("--municipio", default="2511400", help="Código IBGE do município")
    ap.add_argument("--out", default="data/raw/sisu_picui_2017_2022_agg.csv")
    args = ap.parse_args()

    query = build_query(args.ano_ini, args.ano_fim, args.municipio)

    print("Executando consulta no BigQuery via basedosdados...")
    df = bd.read_sql(query=query, billing_project_id=args.billing_project)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False, encoding="utf-8-sig")

    print(f"Arquivo agregado salvo em: {out_path.resolve()}")
    print(f"Linhas retornadas: {len(df)}")


if __name__ == "__main__":
    main()
