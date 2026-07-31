"""
predict_hero.py

Hero da página de simulação e predição.
"""

import streamlit as st


def show_prediction_hero() -> None:
    """
    Exibe o cabeçalho principal da página de predição.
    """

    st.html(
        """
        <section class="hero-section">
            <div class="hero-content">

                <p class="hero-eyebrow">
                    SIMULAÇÃO DE CENÁRIOS
                </p>

                <h1 class="hero-title">
                    Predição da Gravidade de Acidentes
                </h1>

                <p class="hero-subtitle">
                    Estime o risco associado a um cenário rodoviário
                </p>

                <p class="hero-description">
                    Informe as características do local, da via, do ambiente
                    e do veículo para estimar a probabilidade de uma pessoa
                    envolvida em um acidente apresentar lesões graves ou
                    evoluir para óbito.
                </p>

                <div class="hero-indicators">

                    <div class="hero-indicator">
                        <span class="hero-indicator-value">
                            XGBoost
                        </span>

                        <span class="hero-indicator-label">
                            Modelo preditivo
                        </span>
                    </div>

                    <div class="hero-indicator">
                        <span class="hero-indicator-value">
                            Probabilidade
                        </span>

                        <span class="hero-indicator-label">
                            Estimativa individual
                        </span>
                    </div>

                    <div class="hero-indicator">
                        <span class="hero-indicator-value">
                            SHAP
                        </span>

                        <span class="hero-indicator-label">
                            Explicação da previsão
                        </span>
                    </div>

                </div>

            </div>
        </section>
        """
    )