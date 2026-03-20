import argparse
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {"ano", "nome_curso", "turno", "total_inscricoes"}


def load_aggregated_input(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        cols = ", ".join(sorted(missing))
        raise ValueError(f"Arquivo de entrada sem colunas obrigatórias: {cols}")

    df = df.copy()
    df["ano"] = df["ano"].astype(int)
    df["nome_curso"] = df["nome_curso"].fillna("NÃO INFORMADO").astype(str).str.strip()
    df["turno"] = df["turno"].fillna("NÃO INFORMADO").astype(str).str.strip()
    df["total_inscricoes"] = df["total_inscricoes"].fillna(0).astype(int)
    return df


def build_outputs(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    ranking_cursos = (
        df.groupby("nome_curso", as_index=False)["total_inscricoes"]
        .sum()
        .rename(columns={"nome_curso": "curso"})
        .sort_values(["total_inscricoes", "curso"], ascending=[False, True])
        .reset_index(drop=True)
    )

    ranking_turnos = (
        df.groupby("turno", as_index=False)["total_inscricoes"]
        .sum()
        .sort_values(["total_inscricoes", "turno"], ascending=[False, True])
        .reset_index(drop=True)
    )

    ranking_cursos_por_ano = (
        df.groupby(["ano", "nome_curso"], as_index=False)["total_inscricoes"]
        .sum()
        .rename(columns={"nome_curso": "curso"})
        .sort_values(["ano", "total_inscricoes", "curso"], ascending=[True, False, True])
        .reset_index(drop=True)
    )

    ranking_turnos_por_ano = (
        df.groupby(["ano", "turno"], as_index=False)["total_inscricoes"]
        .sum()
        .sort_values(["ano", "total_inscricoes", "turno"], ascending=[True, False, True])
        .reset_index(drop=True)
    )

    return {
        "ranking_cursos_picui_2017_2022": ranking_cursos,
        "ranking_turnos_picui_2017_2022": ranking_turnos,
        "ranking_cursos_por_ano_picui_2017_2022": ranking_cursos_por_ano,
        "ranking_turnos_por_ano_picui_2017_2022": ranking_turnos_por_ano,
    }


def save_outputs(outputs: dict[str, pd.DataFrame], outdir: Path, workbook_name: str) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    for base_name, frame in outputs.items():
        csv_path = outdir / f"{base_name}.csv"
        frame.to_csv(csv_path, index=False, encoding="utf-8-sig")

    workbook_path = outdir / workbook_name
    with pd.ExcelWriter(workbook_path, engine="openpyxl") as writer:
        outputs["ranking_cursos_picui_2017_2022"].to_excel(writer, sheet_name="cursos_total", index=False)
        outputs["ranking_turnos_picui_2017_2022"].to_excel(writer, sheet_name="turnos_total", index=False)
        outputs["ranking_cursos_por_ano_picui_2017_2022"].to_excel(
            writer, sheet_name="cursos_por_ano", index=False
        )
        outputs["ranking_turnos_por_ano_picui_2017_2022"].to_excel(
            writer, sheet_name="turnos_por_ano", index=False
        )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="data/raw/sisu_picui_2017_2022_agg.csv")
    ap.add_argument("--outdir", default="data/processed")
    ap.add_argument("--workbook", default="relatorio_picui_2017_2022.xlsx")
    args = ap.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Arquivo agregado não encontrado: {input_path}")

    df = load_aggregated_input(input_path)
    outputs = build_outputs(df)
    save_outputs(outputs, Path(args.outdir), args.workbook)

    print("Rankings e tabelas gerados em:", Path(args.outdir).resolve())


if __name__ == "__main__":
    main()
