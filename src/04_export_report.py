import argparse
from pathlib import Path

import pandas as pd


def load_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    return pd.read_csv(path)


def dataframe_to_markdown(df: pd.DataFrame, rows: int) -> str:
    return df.head(rows).to_markdown(index=False)


def prepare_markdown_table(df: pd.DataFrame, rows: int, column_map: dict[str, str]) -> str:
    display_df = df.head(rows).rename(columns=column_map).copy()
    for col in display_df.columns:
        if "Inscrições" in col:
            display_df[col] = display_df[col].map(lambda x: f"{int(x):,}".replace(",", "."))
    return display_df.to_markdown(index=False)


def render_report(processed_dir: Path, figures_dir: Path, top_n: int) -> str:
    ranking_cursos = load_table(processed_dir / "ranking_cursos_picui_2017_2022.csv")
    ranking_turnos = load_table(processed_dir / "ranking_turnos_picui_2017_2022.csv")
    cursos_por_ano = load_table(processed_dir / "ranking_cursos_por_ano_picui_2017_2022.csv")
    turnos_por_ano = load_table(processed_dir / "ranking_turnos_por_ano_picui_2017_2022.csv")

    total_inscricoes = int(ranking_cursos["total_inscricoes"].sum())
    anos = sorted(cursos_por_ano["ano"].astype(int).unique().tolist())
    periodo = f"{anos[0]}-{anos[-1]}" if anos else "sem dados"

    figures = [
        figures_dir / "fig1_top15_cursos_picui_2017_2022.png",
        figures_dir / "fig2_turnos_picui_2017_2022.png",
        figures_dir / "fig3_turnos_por_ano_picui_2017_2022.png",
        figures_dir / "fig4_cursos_ifpb_picui_por_ano_2017_2022.png",
    ]

    available_figures = [path for path in figures if path.exists()]

    lines = [
        "# Resumo de resultados",
        "",
        "## Escopo",
        f"- Município analisado: Picuí (PB), código IBGE 2511400",
        f"- Período coberto: {periodo}",
        f"- Unidade analítica: inscrições no SiSU agregadas por ano, curso e turno",
        f"- Total de inscrições no período: {total_inscricoes}",
        "",
        "## Top cursos no período",
        prepare_markdown_table(
            ranking_cursos,
            top_n,
            {"curso": "Curso", "total_inscricoes": "Inscrições"},
        ),
        "",
        "## Preferência por turno no período",
        prepare_markdown_table(
            ranking_turnos,
            len(ranking_turnos),
            {"turno": "Turno", "total_inscricoes": "Inscrições"},
        ),
        "",
        "## Cursos por ano",
        prepare_markdown_table(
            cursos_por_ano,
            top_n,
            {"ano": "Ano", "curso": "Curso", "total_inscricoes": "Inscrições"},
        ),
        "",
        "## Turnos por ano",
        prepare_markdown_table(
            turnos_por_ano,
            len(turnos_por_ano),
            {"ano": "Ano", "turno": "Turno", "total_inscricoes": "Inscrições"},
        ),
        "",
        "## Figuras disponíveis",
    ]

    if available_figures:
        lines.extend(f"- {path.as_posix()}" for path in available_figures)
    else:
        lines.append("- Nenhuma figura encontrada no diretório informado.")

    lines.extend(
        [
            "",
            "## Nota metodológica",
            "- As contagens representam inscrições registradas no SiSU, não matrículas nem permanência.",
            "- O resumo serve como apoio para redação do artigo e deve ser interpretado junto com o enquadramento teórico.",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--processed", default="data/processed")
    ap.add_argument("--figdir", default="docs/paper/figuras")
    ap.add_argument("--out", default="docs/paper/resumo_resultados.md")
    ap.add_argument("--top-n", type=int, default=15)
    args = ap.parse_args()

    processed_dir = Path(args.processed)
    figures_dir = Path(args.figdir)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    report = render_report(processed_dir, figures_dir, args.top_n)
    out_path.write_text(report, encoding="utf-8")

    print("Resumo em Markdown gerado em:", out_path.resolve())


if __name__ == "__main__":
    main()
