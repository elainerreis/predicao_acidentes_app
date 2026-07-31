"""
dashboard_heatmap.py

Mapa de calor do Dashboard.
"""

import plotly.express as px
import streamlit as st


COLOR_SCALE = "YlOrRd"


def heatmap(df, linha, coluna, titulo):
    """
    Exibe um mapa de calor da taxa de gravidade.
    """

    tabela = (
        df.groupby([linha, coluna])
        .agg(
            taxa=("gravidade", "mean"),
        )
        .reset_index()
    )

    matriz = tabela.pivot(
        index=linha,
        columns=coluna,
        values="taxa",
    )

    # Renomeia os eixos
    matriz.index.name = "Dia da Semana"
    matriz.columns.name = "Fase do Dia"

    fig = px.imshow(
        matriz,
        text_auto=".1%",
        color_continuous_scale=COLOR_SCALE,
        aspect="auto",
    )

    fig.update_traces(
        textfont_size=11,
        texttemplate="%{z:.1%}",
    )

    fig.update_layout(
        title=titulo,
        height=500,
        xaxis_title="Fase do Dia",
        yaxis_title="Dia da Semana",
        coloraxis_colorbar_title="Taxa de Gravidade",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )


def show_heatmaps(df):
    """
    Exibe o mapa de calor do Dashboard.
    """

    st.subheader("Mapa de Calor")

    heatmap(
        df,
        "dia_semana",
        "fase_dia",
        "Taxa de Gravidade por Dia da Semana e Fase do Dia",
    )