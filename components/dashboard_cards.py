"""
dashboard_cards.py

Cards de indicadores gerais do Dashboard.
"""

import streamlit as st


def show_dashboard_cards(df):
    """
    Exibe os principais indicadores.
    """

    total_acidentes = len(df)

    acidentes_graves = int(df["gravidade"].sum())

    taxa_gravidade = (
        acidentes_graves / total_acidentes
        if total_acidentes > 0
        else 0
    )

    total_ufs = df["uf"].nunique()

    total_brs = df["br"].nunique()

    st.subheader("Indicadores Gerais")

    col1, col2, col3, col4, col5 = st.columns(
    [1.6, 1.6, 1.2, 0.8, 0.8])

    with col1:

        st.metric(
            "Acidentados",
            f"{total_acidentes:,}".replace(",", "."),
        )

    with col2:

        st.metric(
            "Acidentados Graves",
            f"{acidentes_graves:,}".replace(",", "."),
        )

    with col3:

        st.metric(
            "Taxa de Gravidade",
            f"{taxa_gravidade:.1%}",
        )

    with col4:

        st.metric(
            "UFs",
            total_ufs,
        )

    with col5:

        st.metric(
            "BRs",
            total_brs,
        )