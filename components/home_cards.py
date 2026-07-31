"""
home_cards.py

Resumo do projeto.
"""

import streamlit as st


def show_project_cards():

    st.subheader("Projeto em Números")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Pessoas Acidentadas",
            "+4 milhões",
        )

    with c2:
        st.metric(
            "Variáveis",
            "13",
        )

    with c3:
        st.metric(
            "Modelo",
            "XGBoost",
        )

    with c4:
        st.metric(
            "Interpretabilidade",
            "SHAP",
        )