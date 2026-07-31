"""
Gráficos de barras do Dashboard.

Os gráficos estão organizados de acordo com as seções
narrativas da página:

- Onde os acidentes ocorrem?
- Quando os acidentes acontecem?
- Em quais condições ocorrem?
- Perfil dos veículos envolvidos
"""

import pandas as pd
import plotly.express as px
import streamlit as st


# ======================================================
# CONFIGURAÇÕES
# ======================================================

COLOR = "#1565C0"

TRACADOS = [
    "Aclive",
    "Curva",
    "Declive",
    "Desvio Temporário",
    "Em Obras",
    "Interseção de Vias",
    "Ponte",
    "Reta",
    "Retorno Regulamentado",
    "Rotatória",
    "Túnel",
    "Viaduto",
]

ORDEM_DIAS_SEMANA = [
    "segunda-feira",
    "terça-feira",
    "quarta-feira",
    "quinta-feira",
    "sexta-feira",
    "sábado",
    "domingo",
]

ORDEM_FASE_DIA = [
    "Amanhecer",
    "Pleno dia",
    "Anoitecer",
    "Plena noite",
]


# ======================================================
# FUNÇÕES AUXILIARES
# ======================================================


def resumo_categoria(df: pd.DataFrame, coluna: str) -> pd.DataFrame:
    """
    Calcula quantidade de registros, registros graves,
    taxa de gravidade e participação percentual por categoria.
    """

    if df.empty or coluna not in df.columns:
        return pd.DataFrame(
            columns=[
                coluna,
                "acidentes",
                "graves",
                "taxa",
                "percentual",
            ]
        )

    resumo = (
        df.groupby(
            coluna,
            dropna=False,
            observed=True,
        )
        .agg(
            acidentes=("gravidade", "size"),
            graves=("gravidade", "sum"),
        )
        .reset_index()
    )

    resumo["taxa"] = (
        resumo["graves"]
        / resumo["acidentes"]
    )

    total = resumo["acidentes"].sum()

    resumo["percentual"] = (
        resumo["acidentes"] / total
        if total > 0
        else 0
    )

    return resumo


def _mostrar_aviso_sem_dados():
    """
    Exibe aviso quando não existem registros
    suficientes para gerar o gráfico.
    """

    st.info(
        "Não há dados disponíveis para esta visualização "
        "com os filtros selecionados."
    )


def horizontal_bar(
    resumo: pd.DataFrame,
    coluna: str,
    eixo: str,
    titulo: str,
    top: int | None = None,
    altura: int = 420,
):
    """
    Exibe um gráfico de barras horizontal.
    """

    if (
        resumo.empty
        or coluna not in resumo.columns
        or eixo not in resumo.columns
    ):
        _mostrar_aviso_sem_dados()
        return

    dados = resumo.copy()

    dados[coluna] = (
        dados[coluna]
        .fillna("Não informado")
        .astype(str)
    )

    if top is not None:
        dados = dados.nlargest(top, eixo)

    dados = dados.sort_values(
        eixo,
        ascending=True,
    )

    fig = px.bar(
        dados,
        x=eixo,
        y=coluna,
        orientation="h",
        text=eixo,
        custom_data=[
            "graves",
            "taxa",
            "percentual",
        ]
        if {
            "graves",
            "taxa",
            "percentual",
        }.issubset(dados.columns)
        else None,
    )

    fig.update_traces(
        marker_color=COLOR,
        texttemplate="%{text:,.0f}",
        textposition="outside",
        cliponaxis=False,
    )

    if {
        "graves",
        "taxa",
        "percentual",
    }.issubset(dados.columns):
        fig.update_traces(
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Acidentados: %{x:,.0f}<br>"
                "Acidentados graves: %{customdata[0]:,.0f}<br>"
                "Taxa de gravidade: %{customdata[1]:.1%}<br>"
                "Participação: %{customdata[2]:.1%}"
                "<extra></extra>"
            )
        )

    fig.update_layout(
        title=titulo,
        height=altura,
        showlegend=False,
        separators=",.",
        margin=dict(
            l=10,
            r=50,
            t=55,
            b=20,
        ),
        uniformtext_minsize=10,
        uniformtext_mode="hide",
        xaxis_title="Quantidade de acidentados",
        yaxis_title="",
    )

    fig.update_xaxes(
        tickformat=",",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )


def vertical_bar(
    resumo: pd.DataFrame,
    coluna: str,
    eixo: str,
    titulo: str,
    altura: int = 500,
    ordem: list | None = None,
):
    """
    Exibe um gráfico de barras vertical.
    """

    if (
        resumo.empty
        or coluna not in resumo.columns
        or eixo not in resumo.columns
    ):
        _mostrar_aviso_sem_dados()
        return

    dados = resumo.copy()

    dados[coluna] = (
        dados[coluna]
        .fillna("Não informado")
        .astype(str)
    )

    if ordem is not None:
        categorias_existentes = [
            categoria
            for categoria in ordem
            if categoria in dados[coluna].tolist()
        ]

        categorias_restantes = [
            categoria
            for categoria in dados[coluna].tolist()
            if categoria not in categorias_existentes
        ]

        ordem_final = (
            categorias_existentes
            + categorias_restantes
        )

        dados[coluna] = pd.Categorical(
            dados[coluna],
            categories=ordem_final,
            ordered=True,
        )

        dados = dados.sort_values(coluna)

    else:
        dados = dados.sort_values(
            eixo,
            ascending=False,
        )

    fig = px.bar(
        dados,
        x=coluna,
        y=eixo,
        text=eixo,
        custom_data=[
            "graves",
            "taxa",
            "percentual",
        ]
        if {
            "graves",
            "taxa",
            "percentual",
        }.issubset(dados.columns)
        else None,
    )

    fig.update_traces(
        marker_color=COLOR,
        texttemplate="%{text:,.0f}",
        textposition="outside",
        cliponaxis=False,
    )

    if {
        "graves",
        "taxa",
        "percentual",
    }.issubset(dados.columns):
        fig.update_traces(
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Acidentados: %{y:,.0f}<br>"
                "Acidentados graves: %{customdata[0]:,.0f}<br>"
                "Taxa de gravidade: %{customdata[1]:.1%}<br>"
                "Participação: %{customdata[2]:.1%}"
                "<extra></extra>"
            )
        )

    fig.update_layout(
        title=titulo,
        height=altura,
        showlegend=False,
        separators=",.",
        margin=dict(
            l=10,
            r=10,
            t=55,
            b=30,
        ),
        xaxis_title="",
        yaxis_title="Quantidade de acidentados",
    )

    fig.update_yaxes(
        tickformat=",",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )


# ======================================================
# TRAÇADO DA VIA
# ======================================================


def resumo_tracado(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resume a quantidade de registros para cada
    característica de traçado da via.
    """

    colunas = [
        coluna
        for coluna in TRACADOS
        if coluna in df.columns
    ]

    if df.empty or not colunas:
        return pd.DataFrame(
            columns=[
                "Traçado",
                "Quantidade",
            ]
        )

    dados = (
        df[colunas]
        .apply(
            pd.to_numeric,
            errors="coerce",
        )
        .fillna(0)
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    dados.columns = [
        "Traçado",
        "Quantidade",
    ]

    dados = dados[
        dados["Quantidade"] > 0
    ]

    return dados


def show_tracado(df: pd.DataFrame):
    """
    Exibe a distribuição dos registros por
    característica de traçado da via.
    """

    dados = resumo_tracado(df)

    if dados.empty:
        _mostrar_aviso_sem_dados()
        return

    horizontal_bar(
        resumo=dados,
        coluna="Traçado",
        eixo="Quantidade",
        titulo="Traçado da via",
        altura=460,
    )


# ======================================================
# SEÇÃO 2 — ONDE OS ACIDENTES OCORREM?
# ======================================================


def show_location_charts(df: pd.DataFrame):
    """
    Exibe os gráficos relacionados à localização:

    - distribuição por UF;
    - dez BRs com maior número de registros.
    """

    # ==================================================
    # ACIDENTADOS POR UF
    # ==================================================

    resumo_uf = resumo_categoria(
        df,
        "uf",
    )

    vertical_bar(
        resumo=resumo_uf,
        coluna="uf",
        eixo="acidentes",
        titulo="Distribuição dos acidentados por UF",
        altura=520,
    )

    # ==================================================
    # TOP 10 BRs
    # ==================================================

    resumo_br = resumo_categoria(
        df,
        "br",
    )

    if not resumo_br.empty:

        resumo_br = resumo_br.copy()

        # Garante que a BR seja tratada como categoria,
        # e não como uma escala numérica contínua.
        resumo_br["br"] = (
            resumo_br["br"]
            .astype(str)
            .str.replace(".0", "", regex=False)
            .str.strip()
        )

        # Evita duplicar o prefixo caso já exista.
        resumo_br["br"] = resumo_br["br"].apply(
            lambda valor: (
                valor
                if valor.startswith("BR-")
                else f"BR-{valor.zfill(3)}"
            )
        )

    horizontal_bar(
        resumo=resumo_br,
        coluna="br",
        eixo="acidentes",
        titulo="BRs com maior número de acidentados",
        top=10,
        altura=440,
    )


# ======================================================
# SEÇÃO 3 — QUANDO OS ACIDENTES ACONTECEM?
# ======================================================


def show_time_charts(df: pd.DataFrame):
    """
    Exibe os gráficos temporais:

    - ano;
    - dia da semana;
    - fase do dia.
    """

    resumo_ano = resumo_categoria(
        df,
        "ano",
    )

    if not resumo_ano.empty:
        resumo_ano["ano"] = (
            pd.to_numeric(
                resumo_ano["ano"],
                errors="coerce",
            )
            .astype("Int64")
            .astype(str)
        )

        resumo_ano = resumo_ano.sort_values(
            "ano"
        )

    vertical_bar(
        resumo=resumo_ano,
        coluna="ano",
        eixo="acidentes",
        titulo="Evolução dos registros por ano",
        altura=430,
        ordem=(
            resumo_ano["ano"].tolist()
            if not resumo_ano.empty
            else None
        ),
    )

    col1, col2 = st.columns(2)

    with col1:
        resumo_dia = resumo_categoria(
            df,
            "dia_semana",
        )

        horizontal_bar(
            resumo=resumo_dia,
            coluna="dia_semana",
            eixo="acidentes",
            titulo="Distribuição por dia da semana",
            altura=440,
        )

    with col2:
        resumo_fase = resumo_categoria(
            df,
            "fase_dia",
        )

        horizontal_bar(
            resumo=resumo_fase,
            coluna="fase_dia",
            eixo="acidentes",
            titulo="Distribuição por fase do dia",
            altura=440,
        )


# ======================================================
# SEÇÃO 4 — EM QUAIS CONDIÇÕES?
# ======================================================


def show_conditions_charts(df: pd.DataFrame):
    """
    Exibe gráficos relacionados às condições
    ambientais e às características da via:

    - tipo de pista;
    - condição meteorológica;
    - perímetro urbano;
    - traçado da via.
    """

    # Primeira linha
    col1, col2 = st.columns(2)

    with col1:
        resumo_pista = resumo_categoria(
            df,
            "tipo_pista",
        )

        horizontal_bar(
            resumo=resumo_pista,
            coluna="tipo_pista",
            eixo="acidentes",
            titulo="Distribuição por tipo de pista",
            altura=440,
        )

    with col2:
        resumo_clima = resumo_categoria(
            df,
            "condicao_metereologica",
        )

        horizontal_bar(
            resumo=resumo_clima,
            coluna="condicao_metereologica",
            eixo="acidentes",
            titulo="Distribuição por condição meteorológica",
            altura=440,
        )

    # Segunda linha
    col3, col4 = st.columns(2)

    with col3:
        resumo_perimetro = resumo_categoria(
            df,
            "uso_solo",
        )

        horizontal_bar(
            resumo=resumo_perimetro,
            coluna="uso_solo",
            eixo="acidentes",
            titulo="Distribuição por perímetro urbano",
            altura=440,
        )

    with col4:
        show_tracado(df)


# ======================================================
# SEÇÃO 5 — PERFIL DOS VEÍCULOS
# ======================================================


def show_vehicle_chart(df: pd.DataFrame):
    """
    Exibe os tipos de veículo com maior número
    de pessoas envolvidas nos registros.
    """

    resumo_veiculo = resumo_categoria(
        df,
        "tipo_veiculo",
    )

    horizontal_bar(
        resumo=resumo_veiculo,
        coluna="tipo_veiculo",
        eixo="acidentes",
        titulo="Tipos de veículo mais frequentes",
        top=12,
        altura=520,
    )


# ======================================================
# FUNÇÃO TEMPORÁRIA DE COMPATIBILIDADE
# ======================================================


def show_bar_charts(df: pd.DataFrame):
    """
    Mantém compatibilidade com a versão anterior
    enquanto dashboard.py ainda não for reorganizado.

    Depois que a nova página estiver pronta,
    esta função poderá ser removida.
    """

    show_location_charts(df)

    st.divider()

    show_time_charts(df)

    st.divider()

    show_conditions_charts(df)

    st.divider()

    show_vehicle_chart(df)