from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
FIGURES_DIR = ROOT / "docs" / "paper" / "figuras"

ACCENT = "#1f4e5f"
ACCENT_SOFT = "#e7f0f3"
INK = "#1f2933"
MUTED = "#52606d"


st.set_page_config(
    page_title="SiSU Picuí",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data() -> dict[str, pd.DataFrame]:
    cursos_total = pd.read_csv(PROCESSED_DIR / "ranking_cursos_picui_2017_2022.csv")
    turnos_total = pd.read_csv(PROCESSED_DIR / "ranking_turnos_picui_2017_2022.csv")
    cursos_ano = pd.read_csv(PROCESSED_DIR / "ranking_cursos_por_ano_picui_2017_2022.csv")
    turnos_ano = pd.read_csv(PROCESSED_DIR / "ranking_turnos_por_ano_picui_2017_2022.csv")

    cursos_total["curso"] = cursos_total["curso"].astype(str).str.strip()
    turnos_total["turno"] = turnos_total["turno"].astype(str).str.strip()
    cursos_ano["curso"] = cursos_ano["curso"].astype(str).str.strip()
    turnos_ano["turno"] = turnos_ano["turno"].astype(str).str.strip()

    cursos_total = (
        cursos_total.groupby("curso", as_index=False)["total_inscricoes"]
        .sum()
        .sort_values(["total_inscricoes", "curso"], ascending=[False, True])
        .reset_index(drop=True)
    )
    turnos_total = (
        turnos_total.groupby("turno", as_index=False)["total_inscricoes"]
        .sum()
        .sort_values(["total_inscricoes", "turno"], ascending=[False, True])
        .reset_index(drop=True)
    )
    cursos_ano = (
        cursos_ano.groupby(["ano", "curso"], as_index=False)["total_inscricoes"]
        .sum()
        .sort_values(["ano", "total_inscricoes", "curso"], ascending=[True, False, True])
        .reset_index(drop=True)
    )
    turnos_ano = (
        turnos_ano.groupby(["ano", "turno"], as_index=False)["total_inscricoes"]
        .sum()
        .sort_values(["ano", "total_inscricoes", "turno"], ascending=[True, False, True])
        .reset_index(drop=True)
    )

    return {
        "cursos_total": cursos_total,
        "turnos_total": turnos_total,
        "cursos_ano": cursos_ano,
        "turnos_ano": turnos_ano,
    }


def inject_styles() -> None:
    st.markdown(
        f"""
        <style>
            .stApp {{
                background: linear-gradient(180deg, #eef2f5 0%, #e3e8ee 100%);
                color: {INK};
            }}
            .block-container {{
                padding-top: 2rem;
                padding-bottom: 3rem;
            }}
            h1, h2, h3, h4, h5, h6, p, li, label, span, div {{
                color: {INK};
            }}
            [data-testid="stMetricValue"] {{
                color: {INK};
            }}
            [data-testid="stMetricLabel"] {{
                color: {MUTED};
            }}
            [data-testid="stMetricDelta"] {{
                color: {ACCENT};
            }}
            button[role="tab"] {{
                color: {INK};
            }}
            button[role="tab"][aria-selected="true"] {{
                color: {ACCENT};
            }}
            [data-testid="stSidebar"] * {{
                color: #102a43;
            }}
            [data-testid="stSidebar"] {{
                background: #f3f6f9;
            }}
            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
                color: #102a43;
            }}
            [data-testid="stSidebar"] label {{
                color: #102a43 !important;
            }}
            [data-testid="stSidebar"] .stSlider p {{
                color: #102a43 !important;
            }}
            [data-testid="stSidebar"] .stMultiSelect label {{
                color: #102a43 !important;
            }}
            .hero {{
                background: linear-gradient(135deg, {ACCENT} 0%, #2f6f89 100%);
                color: white;
                padding: 2rem 2.2rem;
                border-radius: 20px;
                margin-bottom: 1rem;
                box-shadow: 0 18px 40px rgba(31, 78, 95, 0.18);
            }}
            .hero h1 {{
                margin: 0;
                font-size: 2.3rem;
                line-height: 1.1;
                color: #f8fbfc;
            }}
            .hero p {{
                margin-top: 0.8rem;
                font-size: 1rem;
                max-width: 58rem;
                color: #f8fbfc;
            }}
            .section-note {{
                background: {ACCENT_SOFT};
                border-left: 6px solid {ACCENT};
                padding: 1rem 1.1rem;
                border-radius: 12px;
                color: {INK};
                margin-bottom: 1rem;
            }}
            .finding-card {{
                background: white;
                border: 1px solid #d9e2ec;
                border-radius: 16px;
                padding: 1rem;
                min-height: 165px;
                box-shadow: 0 10px 22px rgba(15, 23, 42, 0.05);
            }}
            .finding-kicker {{
                color: {MUTED};
                font-size: 0.78rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin-bottom: 0.4rem;
            }}
            .finding-title {{
                color: {ACCENT};
                font-size: 1.25rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
            }}
            .caption {{
                color: {MUTED};
                font-size: 0.92rem;
                margin-top: -0.3rem;
                margin-bottom: 0.9rem;
            }}
            .compact-table {{
                font-size: 0.89rem;
            }}
            [data-testid="stCodeBlock"] pre {{
                background: #f8fafc !important;
                color: #102a43 !important;
                border: 1px solid #d9e2ec;
            }}
            [data-testid="stCodeBlock"] code {{
                color: #102a43 !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def aggregate_for_years(df: pd.DataFrame, group_col: str, years: list[int]) -> pd.DataFrame:
    filtered = df[df["ano"].isin(years)].copy()
    result = (
        filtered.groupby(group_col, as_index=False)["total_inscricoes"]
        .sum()
        .sort_values(["total_inscricoes", group_col], ascending=[False, True])
        .reset_index(drop=True)
    )
    return result


def format_int(value: int) -> str:
    return f"{int(value):,}".replace(",", ".")


def prepare_display_table(df: pd.DataFrame, column_map: dict[str, str]) -> pd.DataFrame:
    display_df = df.rename(columns=column_map).copy()
    for col in display_df.columns:
        if "Inscrições" in col:
            display_df[col] = display_df[col].map(format_int)
        if "Participação" in col:
            display_df[col] = display_df[col].map(lambda x: f"{x:.2f}%")
    return display_df


def compute_story_metrics(data: dict[str, pd.DataFrame], years: list[int]) -> dict[str, object]:
    cursos = aggregate_for_years(data["cursos_ano"], "curso", years)
    turnos = aggregate_for_years(data["turnos_ano"], "turno", years)
    cursos_series = data["cursos_ano"][data["cursos_ano"]["ano"].isin(years)].copy()
    turnos_series = data["turnos_ano"][data["turnos_ano"]["ano"].isin(years)].copy()

    total = int(cursos["total_inscricoes"].sum())
    top_course = cursos.iloc[0]
    top_three = int(cursos.head(3)["total_inscricoes"].sum())
    top_three_share = round((top_three / total) * 100, 1) if total else 0

    integral = int(turnos.loc[turnos["turno"] == "Integral", "total_inscricoes"].sum())
    noturno = int(turnos.loc[turnos["turno"] == "Noturno", "total_inscricoes"].sum())
    integral_share = round((integral / total) * 100, 1) if total else 0
    noturno_share = round((noturno / total) * 100, 1) if total else 0

    ano_inicio = min(years)
    ano_fim = max(years)
    integral_inicio = int(
        turnos_series[
            (turnos_series["ano"] == ano_inicio) & (turnos_series["turno"] == "Integral")
        ]["total_inscricoes"].sum()
    )
    integral_fim = int(
        turnos_series[
            (turnos_series["ano"] == ano_fim) & (turnos_series["turno"] == "Integral")
        ]["total_inscricoes"].sum()
    )
    delta_integral = integral_fim - integral_inicio

    return {
        "cursos": cursos,
        "turnos": turnos,
        "cursos_series": cursos_series,
        "turnos_series": turnos_series,
        "total": total,
        "top_course_name": str(top_course["curso"]),
        "top_course_total": int(top_course["total_inscricoes"]),
        "top_three_share": top_three_share,
        "integral_share": integral_share,
        "noturno_share": noturno_share,
        "delta_integral": delta_integral,
    }


def render_hero(years: list[int], metrics: dict[str, object]) -> None:
    st.markdown(
        f"""
        <div class="hero">
            <h1>SiSU Picuí: preferências territoriais, cursos e turnos</h1>
            <p>
                Painel de apresentação para discutir como residentes de Picuí (PB) distribuem suas
                inscrições no SiSU entre {min(years)} e {max(years)}. A leitura proposta aqui é
                exploratória e serve de apoio a uma discussão sobre mobilidade territorial e
                não adesão, sem confundir inscrição com matrícula ou evasão.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Inscrições no recorte", format_int(metrics["total"]))
    col2.metric(
        "Curso mais frequente",
        str(metrics["top_course_name"]),
        f'{format_int(metrics["top_course_total"])} inscrições',
    )
    col3.metric("Peso do turno integral", f'{metrics["integral_share"]}%')
    col4.metric("Peso do top 3 de cursos", f'{metrics["top_three_share"]}%')


def render_findings(metrics: dict[str, object]) -> None:
    st.subheader("Achados centrais")
    st.markdown(
        '<div class="section-note">Os pontos abaixo sintetizam padrões observáveis no conjunto de inscrições e servem como entrada para a interpretação analítica do material.</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="finding-card">
                <div class="finding-kicker">Achado 1</div>
                <div class="finding-title">Concentração relativa das escolhas</div>
                <div>
                    O curso com maior volume no recorte é <strong>{metrics["top_course_name"]}</strong>,
                    com <strong>{format_int(metrics["top_course_total"])}</strong> inscrições.
                    Os três cursos mais frequentes concentram <strong>{metrics["top_three_share"]}%</strong>
                    do total observado.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="finding-card">
                <div class="finding-kicker">Achado 2</div>
                <div class="finding-title">Predomínio do turno integral</div>
                <div>
                    O turno integral responde por <strong>{metrics["integral_share"]}%</strong>
                    das inscrições no recorte, acima do noturno, que aparece com
                    <strong>{metrics["noturno_share"]}%</strong>.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        delta_label = "queda" if metrics["delta_integral"] < 0 else "crescimento"
        st.markdown(
            f"""
            <div class="finding-card">
                <div class="finding-kicker">Achado 3</div>
                <div class="finding-title">Mudança temporal do integral</div>
                <div>
                    Entre o primeiro e o último ano do recorte, o volume de inscrições em cursos
                    integrais mostra <strong>{delta_label}</strong> de
                    <strong>{format_int(abs(metrics["delta_integral"]))}</strong> registros.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def show_overview(metrics: dict[str, object], top_n: int) -> None:
    render_findings(metrics)

    col1, col2 = st.columns((1.35, 1))
    with col1:
        st.subheader(f"Distribuição das preferências por curso no recorte selecionado")
        st.markdown(
            '<div class="caption">O gráfico mostra os cursos com maior volume de inscrições no recorte selecionado, permitindo observar concentração relativa de preferências entre áreas de formação.</div>',
            unsafe_allow_html=True,
        )
        chart_df = metrics["cursos"].head(top_n).set_index("curso")
        st.bar_chart(chart_df["total_inscricoes"], height=430)

    with col2:
        st.subheader("Composição das inscrições por turno")
        st.markdown(
            '<div class="caption">A distribuição por turno permite observar o peso relativo das diferentes formas de organização temporal associadas às inscrições registradas no SiSU.</div>',
            unsafe_allow_html=True,
        )
        chart_df = metrics["turnos"].set_index("turno")
        st.bar_chart(chart_df["total_inscricoes"], height=430)

    st.subheader("Tabela-síntese para citação rápida")
    summary = metrics["cursos"].head(top_n).copy()
    summary["participação_no_total"] = ((summary["total_inscricoes"] / metrics["total"]) * 100).round(2)
    st.dataframe(
        prepare_display_table(
            summary,
            {
                "curso": "Curso",
                "total_inscricoes": "Inscrições",
                "participação_no_total": "Participação no total",
            },
        ),
        use_container_width=True,
        hide_index=True,
    )


def show_courses(metrics: dict[str, object], top_n: int) -> None:
    st.subheader("Série anual dos cursos em destaque")
    st.markdown(
        '<div class="caption">A série temporal permite observar oscilações anuais que ficam menos visíveis no ranking agregado do período.</div>',
        unsafe_allow_html=True,
    )

    selected_courses = metrics["cursos"].head(top_n)["curso"].tolist()
    filtered_series = metrics["cursos_series"][metrics["cursos_series"]["curso"].isin(selected_courses)]
    pivot = filtered_series.pivot_table(index="ano", columns="curso", values="total_inscricoes", aggfunc="sum").fillna(0)
    st.line_chart(pivot, height=430)

    st.subheader("Cursos mais recorrentes no período")
    st.dataframe(
        prepare_display_table(
            metrics["cursos"].head(top_n),
            {"curso": "Curso", "total_inscricoes": "Inscrições"},
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Série completa por curso")
    st.dataframe(
        prepare_display_table(
            metrics["cursos_series"],
            {"ano": "Ano", "curso": "Curso", "total_inscricoes": "Inscrições"},
        ),
        use_container_width=True,
        hide_index=True,
    )


def show_turnos(metrics: dict[str, object]) -> None:
    st.subheader("Série anual das inscrições por turno")
    st.markdown(
        '<div class="caption">A evolução temporal por turno permite identificar continuidades e inflexões na distribuição das inscrições ao longo do período analisado.</div>',
        unsafe_allow_html=True,
    )

    pivot = metrics["turnos_series"].pivot_table(
        index="ano", columns="turno", values="total_inscricoes", aggfunc="sum"
    ).fillna(0)
    st.line_chart(pivot, height=430)

    col1, col2 = st.columns((1, 1))
    with col1:
        st.subheader("Turnos no recorte")
        st.markdown('<div class="compact-table">', unsafe_allow_html=True)
        st.dataframe(
            prepare_display_table(
                metrics["turnos"],
                {"turno": "Turno", "total_inscricoes": "Inscrições"},
            ),
            use_container_width=True,
            hide_index=True,
            height=420,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.subheader("Série anual de turnos")
        st.markdown('<div class="compact-table">', unsafe_allow_html=True)
        st.dataframe(
            prepare_display_table(
                metrics["turnos_series"],
                {"ano": "Ano", "turno": "Turno", "total_inscricoes": "Inscrições"},
            ),
            use_container_width=True,
            hide_index=True,
            height=420,
        )
        st.markdown("</div>", unsafe_allow_html=True)


def show_methodology(years: list[int]) -> None:
    st.subheader("Notas metodológicas")
    st.markdown(
        """
        - Fonte: microdados do SiSU consultados via BigQuery e biblioteca `basedosdados`.
        - Recorte territorial: residentes em Picuí (PB), código IBGE `2511400`.
        - Janela temporal usada neste painel: `{}-{}`.
        - Unidade analítica: inscrições agregadas por ano, curso e turno.
        - Cuidado interpretativo: o painel organiza preferências registradas em inscrições e não mede, sozinho, matrícula, permanência ou evasão.
        """.format(min(years), max(years))
    )

    st.subheader("Critérios de leitura")
    st.markdown(
        """
        1. As contagens representam inscrições registradas no SiSU, e não indivíduos únicos.
        2. O painel descreve preferências declaradas por curso e turno entre residentes de Picuí (PB).
        3. As tabelas e séries temporais devem ser lidas como base descritiva para a discussão analítica do artigo.
        4. Inferências sobre permanência, abandono ou evasão exigem articulação com outras bases e outros níveis de análise.
        """
    )

    st.subheader("Fluxo técnico")
    st.code(
        "\n".join(
            [
                "python src/01_extract_sisu.py --billing-project SEU_PROJETO_GCP",
                "python src/02_aggregate_rankings.py",
                "python src/03_generate_figures.py",
                "python src/04_export_report.py",
                "streamlit run dashboard/app.py",
            ]
        ),
        language="bash",
    )

    st.subheader("Material editorial derivado")
    st.markdown(
        """
        As figuras estáticas seguem úteis como produtos de redação do artigo, mas não são o núcleo deste painel.
        No app, a prioridade é a leitura analítica interativa. As saídas fixas permanecem no pipeline para uso no
        artigo escrito e em material suplementar.
        """
    )


def show_conclusions(metrics: dict[str, object], years: list[int]) -> None:
    st.subheader("Conclusões e implicações")
    st.markdown(
        '<div class="section-note">Esta seção reúne uma síntese interpretativa do painel e explicita suas implicações analíticas e seus limites de inferência.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        **1. As inscrições sugerem padrões consistentes de preferência, e não um quadro aleatório de escolhas.**
        Entre {min(years)} e {max(years)}, o volume de inscrições concentra-se em alguns cursos e em determinados
        regimes de turno, o que sugere racionalidades de escolha relativamente estruturadas.

        **2. O predomínio do turno integral merece leitura territorial e social.**
        Com participação de **{metrics["integral_share"]}%** no recorte, o turno integral aparece como eixo central
        das inscrições observadas. Isso abre espaço para discutir condições de deslocamento, expectativa de formação
        e disponibilidade temporal dos estudantes.

        **3. A distribuição por curso e turno reforça a utilidade da hipótese de não adesão territorial.**
        Em vez de supor automaticamente evasão como fracasso individual ou institucional, os dados podem ser lidos
        como indícios de mobilidade orientada por expectativas educacionais, oferta de cursos e organização do tempo.
        """
    )

    st.subheader("Implicações para o argumento do artigo")
    st.markdown(
        """
        - Tratar inscrição como preferência declarada permite qualificar melhor o debate sobre acesso e circulação educacional.
        - O painel sugere que a discussão sobre evasão precisa ser articulada com território, oferta institucional e regime de estudos.
        - A análise ganha força quando diferencia ausência de permanência de ausência de interesse ou de adesão.
        """
    )

    st.subheader("Cuidado interpretativo")
    st.markdown(
        """
        - Este painel não mede matrícula, permanência nem conclusão.
        - As evidências aqui apresentadas funcionam como base empírica para uma interpretação teórica, e não como prova isolada de evasão ou permanência.
        - O passo seguinte no artigo é justamente converter esses padrões descritivos em argumento sociológico e educacional mais robusto.
        """
    )


def main() -> None:
    inject_styles()
    data = load_data()
    all_years = sorted(data["cursos_ano"]["ano"].astype(int).unique().tolist())

    st.sidebar.header("Controles da apresentação")
    years = st.sidebar.multiselect("Anos", options=all_years, default=all_years)
    if not years:
        years = all_years

    top_n = st.sidebar.slider("Cursos em destaque", min_value=5, max_value=20, value=10)

    metrics = compute_story_metrics(data, years)

    render_hero(years, metrics)

    tabs = st.tabs(["Narrativa", "Cursos", "Turnos", "Metodologia", "Conclusões"])

    with tabs[0]:
        show_overview(metrics, top_n)

    with tabs[1]:
        show_courses(metrics, top_n)

    with tabs[2]:
        show_turnos(metrics)

    with tabs[3]:
        show_methodology(years)

    with tabs[4]:
        show_conclusions(metrics, years)


if __name__ == "__main__":
    main()
