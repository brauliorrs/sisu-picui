import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_barh(df: pd.DataFrame, ycol: str, xcol: str, title: str, outpath: Path, topn: int | None = None) -> None:
    plot_df = df.copy()
    if topn is not None:
        plot_df = plot_df.head(topn)
    plot_df = plot_df.sort_values(xcol, ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(plot_df[ycol], plot_df[xcol], color="#2f6f89")
    plt.title(title)
    plt.xlabel("Total de inscrições")
    plt.tight_layout()
    outpath.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(outpath, dpi=200)
    plt.close()


def save_turnos_por_ano(df_turnos_ano: pd.DataFrame, outpath: Path) -> None:
    pivot = (
        df_turnos_ano.pivot_table(index="ano", columns="turno", values="total_inscricoes", aggfunc="sum")
        .fillna(0)
        .sort_index()
    )

    plt.figure(figsize=(10, 6))
    for col in pivot.columns:
        plt.plot(pivot.index, pivot[col], marker="o", label=col)
    plt.title("Evolução anual da preferência por turno (Picuí, 2017-2022)")
    plt.xlabel("Ano")
    plt.ylabel("Total de inscrições")
    plt.legend()
    plt.tight_layout()
    outpath.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(outpath, dpi=200)
    plt.close()


def save_ifpb_cursos_por_ano(df_cursos_ano: pd.DataFrame, cursos_ifpb: list[str], outpath: Path) -> None:
    subset = df_cursos_ano[df_cursos_ano["curso"].isin(cursos_ifpb)].copy()
    pivot = (
        subset.pivot_table(index="ano", columns="curso", values="total_inscricoes", aggfunc="sum")
        .fillna(0)
        .sort_index()
    )

    plt.figure(figsize=(10, 6))
    for col in pivot.columns:
        plt.plot(pivot.index, pivot[col], marker="o", label=col)
    plt.title("Evolução anual das escolhas nos cursos do IFPB-Picuí")
    plt.xlabel("Ano")
    plt.ylabel("Total de inscrições")
    plt.legend()
    plt.tight_layout()
    outpath.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(outpath, dpi=200)
    plt.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--processed", default="data/processed")
    ap.add_argument("--figdir", default="docs/paper/figuras")
    args = ap.parse_args()

    processed = Path(args.processed)
    figdir = Path(args.figdir)

    ranking_cursos = pd.read_csv(processed / "ranking_cursos_picui_2017_2022.csv")
    ranking_turnos = pd.read_csv(processed / "ranking_turnos_picui_2017_2022.csv")
    cursos_por_ano = pd.read_csv(processed / "ranking_cursos_por_ano_picui_2017_2022.csv")
    turnos_por_ano = pd.read_csv(processed / "ranking_turnos_por_ano_picui_2017_2022.csv")

    save_barh(
        ranking_cursos,
        ycol="curso",
        xcol="total_inscricoes",
        title="Top 15 cursos escolhidos por residentes de Picuí (2017-2022)",
        outpath=figdir / "fig1_top15_cursos_picui_2017_2022.png",
        topn=15,
    )

    save_barh(
        ranking_turnos,
        ycol="turno",
        xcol="total_inscricoes",
        title="Preferência por turno em Picuí (2017-2022)",
        outpath=figdir / "fig2_turnos_picui_2017_2022.png",
    )

    save_turnos_por_ano(turnos_por_ano, figdir / "fig3_turnos_por_ano_picui_2017_2022.png")

    cursos_ifpb = ["AGROECOLOGIA", "GESTÃO AMBIENTAL", "GEOGRAFIA", "LETRAS - LÍNGUA PORTUGUESA"]
    save_ifpb_cursos_por_ano(cursos_por_ano, cursos_ifpb, figdir / "fig4_cursos_ifpb_picui_por_ano_2017_2022.png")

    print("Figuras geradas em:", figdir.resolve())


if __name__ == "__main__":
    main()
