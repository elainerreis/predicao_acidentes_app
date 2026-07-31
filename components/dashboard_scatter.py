"""
dashboard_scatter.py

Gráfico de dispersão entre total de acidentes
e taxa de gravidade por UF.
"""

import plotly.express as px
import streamlit as st


COLOR = "#1565C0"


def resumo(df, coluna):
    """
    Calcula total de acidentes e taxa de gravidade.
    """

    dados = (
        df.groupby(coluna)
        .agg(
            acidentes=("gravidade", "size"),
            graves=("gravidade", "sum"),
        )
        .reset_index()
    )

    dados["taxa"] = (
        dados["graves"]
        / dados["acidentes"]
    )

    return dados


def show_scatter_charts(df):
    """
    Exibe o gráfico de dispersão por UF.
    """

    st.subheader("Relação entre Frequência e Gravidade")

    dados = resumo(df, "uf")

    fig = px.scatter(
        dados,
        x="acidentes",
        y="taxa",
        text="uf",
        size="acidentes",
        size_max=18,          # reduz o tamanho máximo das bolhas
    )

    fig.update_traces(
        marker=dict(
            color=COLOR,
            opacity=0.70,
            line=dict(
                color="white",
                width=1,
            ),
        ),
        textposition="top center",
        textfont=dict(size=11),
    )

    fig.update_layout(
        title="Total de Acidentados × Taxa de Gravidade por UF",
        xaxis_title="Total de acidentados",
        yaxis_title="Taxa de gravidade",
        showlegend=False,
        height=600,
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20,
        ),
    )

    fig.update_yaxes(
        tickformat=".0%",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )