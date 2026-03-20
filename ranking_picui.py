import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run_step(script: str, extra_args: list[str]) -> None:
    script_path = ROOT / "src" / script
    cmd = [sys.executable, str(script_path), *extra_args]
    subprocess.run(cmd, check=True, cwd=ROOT)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Executa o pipeline completo do projeto sisu-picui."
    )
    ap.add_argument("--billing-project", required=True, help="Projeto de billing do BigQuery")
    ap.add_argument("--ano-ini", type=int, default=2017)
    ap.add_argument("--ano-fim", type=int, default=2022)
    ap.add_argument("--municipio", default="2511400")
    args = ap.parse_args()

    common_args = [
        "--ano-ini",
        str(args.ano_ini),
        "--ano-fim",
        str(args.ano_fim),
        "--municipio",
        args.municipio,
    ]

    run_step("01_extract_sisu.py", ["--billing-project", args.billing_project, *common_args])
    run_step("02_aggregate_rankings.py", [])
    run_step("03_generate_figures.py", [])
    run_step("04_export_report.py", [])

    print("Pipeline completo executado com sucesso.")


if __name__ == "__main__":
    main()
