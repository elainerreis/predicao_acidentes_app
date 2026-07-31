"""
home_features.py

Apresenta os principais recursos disponíveis na aplicação.
"""

import streamlit as st


def show_features() -> None:
    """Exibe os acessos principais ao Dashboard e à Predição."""

    st.markdown("## Funcionalidades")

    st.markdown(
        """
        A aplicação foi organizada em duas áreas principais: exploração dos
        dados históricos e simulação de novos cenários.
        """
    )

    col_dashboard, col_predicao = st.columns(2, gap="large")

    with col_dashboard:
        st.html(
            """
            <article class="feature-card">
                <p class="feature-card-label">ANÁLISE EXPLORATÓRIA</p>

                <h3 class="feature-card-title">Dashboard</h3>

                <p class="feature-card-text">
                    Explore os registros históricos por meio de indicadores,
                    filtros e visualizações interativas sobre localização,
                    veículos, condições da via e gravidade dos acidentes.
                </p>
            </article>
            """
        )

        st.page_link(
            "pages/dashboard.py",
            label="Acessar o Dashboard",
            use_container_width=True,
        )

    with col_predicao:
        st.html(
            """
            <article class="feature-card">
                <p class="feature-card-label">SIMULAÇÃO DE CENÁRIOS</p>

                <h3 class="feature-card-title">Predição</h3>

                <p class="feature-card-text">
                    Informe as características de um novo cenário, estime a
                    probabilidade de gravidade e visualize os fatores que mais
                    influenciaram a previsão por meio do SHAP.
                </p>
            </article>
            """
        )

        st.page_link(
            "pages/predict.py",
            label="Realizar uma Predição",
            use_container_width=True,
        )