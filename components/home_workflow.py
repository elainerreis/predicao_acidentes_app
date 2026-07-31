"""
home_workflow.py

Apresenta o fluxo metodológico da solução desenvolvida no TCC.
"""

import streamlit as st


def show_workflow() -> None:
    """
    Exibe as etapas da solução, desde a obtenção dos dados
    até a disponibilização dos resultados na aplicação.
    """

    st.markdown("## Fluxo da Solução")

    st.markdown(
        """
        A solução foi construída como um pipeline completo, conectando a
        preparação dos dados ao treinamento, à avaliação e à interpretação
        do modelo preditivo.
        """
    )

    (
        col_dados,
        col_seta_1,
        col_tratamento,
        col_seta_2,
        col_modelo,
        col_seta_3,
        col_shap,
        col_seta_4,
        col_aplicacao,
    ) = st.columns(
        [2.2, 0.35, 2.2, 0.35, 2.2, 0.35, 2.2, 0.35, 2.2],
        gap="small",
    )

    with col_dados:
        st.html(
            """
            <article class="workflow-card">
                <p class="workflow-step">ETAPA 01</p>

                <h3 class="workflow-title">
                    Dados Públicos
                </h3>

                <p class="workflow-text">
                    Registros da Polícia Rodoviária Federal e dados de frota
                    de veículos por município.
                </p>
            </article>
            """
        )

    with col_seta_1:
        st.html('<div class="workflow-arrow">→</div>')

    with col_tratamento:
        st.html(
            """
            <article class="workflow-card">
                <p class="workflow-step">ETAPA 02</p>

                <h3 class="workflow-title">
                    Tratamento
                </h3>

                <p class="workflow-text">
                    Limpeza, integração das bases, tratamento de valores
                    ausentes e engenharia de atributos.
                </p>
            </article>
            """
        )

    with col_seta_2:
        st.html('<div class="workflow-arrow">→</div>')

    with col_modelo:
        st.html(
            """
            <article class="workflow-card">
                <p class="workflow-step">ETAPA 03</p>

                <h3 class="workflow-title">
                    Modelagem
                </h3>

                <p class="workflow-text">
                    Treinamento e avaliação do XGBoost para estimar a
                    probabilidade de gravidade.
                </p>
            </article>
            """
        )

    with col_seta_3:
        st.html('<div class="workflow-arrow">→</div>')

    with col_shap:
        st.html(
            """
            <article class="workflow-card">
                <p class="workflow-step">ETAPA 04</p>

                <h3 class="workflow-title">
                    Interpretabilidade
                </h3>

                <p class="workflow-text">
                    Aplicação do SHAP para compreender a contribuição das
                    variáveis nas previsões.
                </p>
            </article>
            """
        )

    with col_seta_4:
        st.html('<div class="workflow-arrow">→</div>')

    with col_aplicacao:
        st.html(
            """
            <article class="workflow-card">
                <p class="workflow-step">ETAPA 05</p>

                <h3 class="workflow-title">
                    Aplicação
                </h3>

                <p class="workflow-text">
                    Dashboard analítico e ambiente para simulação e
                    interpretação de novos cenários.
                </p>
            </article>
            """
        )