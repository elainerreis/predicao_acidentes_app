"""
home_hero.py

Apresenta a introdução institucional da aplicação e um resumo
dos principais elementos do projeto.
"""

import streamlit as st


def show_hero() -> None:
    """Exibe o Hero da aplicação e a seção Sobre o Projeto."""

    st.html(
        """
        <section class="hero-section">
            <div class="hero-content">

                <h1 class="hero-title">
                    Predição da Gravidade de Acidentes
                    em Rodovias Federais Brasileiras
                </h1>

                <p class="hero-subtitle">
                    Dos Dados ao Alerta
                </p>

                <p class="hero-description">
                    Aplicação desenvolvida para analisar acidentes em rodovias
                    federais e estimar a probabilidade de ocorrência de lesões
                    graves ou óbito por meio de Machine Learning e Inteligência
                    Artificial Explicável.
                </p>

                <div class="hero-indicators">
                    <div class="hero-indicator">
                        <span class="hero-indicator-value">2017–2025</span>
                        <span class="hero-indicator-label">
                            Período analisado
                        </span>
                    </div>

                    <div class="hero-indicator">
                        <span class="hero-indicator-value">
                            Mais de 4 milhões
                        </span>
                        <span class="hero-indicator-label">
                            Registros processados
                        </span>
                    </div>

                    <div class="hero-indicator">
                        <span class="hero-indicator-value">
                            XGBoost e SHAP
                        </span>
                        <span class="hero-indicator-label">
                            Predição e interpretabilidade
                        </span>
                    </div>
                </div>
            </div>
        </section>
        """
    )

    st.markdown("## Sobre o Projeto")

    st.markdown(
        """
        O projeto integra dados públicos, técnicas de Ciência de Dados e
        Machine Learning para investigar os fatores associados à gravidade
        dos acidentes registrados nas rodovias federais brasileiras.
        """
    )

    col_base, col_objetivo = st.columns(2, gap="large")

    with col_base:
        st.html(
            """
            <article class="about-card">
                <p class="about-card-label">01</p>
                <h3 class="about-card-title">Base de Dados</h3>
                <p class="about-card-text">
                    Bases de acidentes disponibilizados pela Polícia
                    Rodoviária Federal, segregadas por pessoa envolvida no acidente, integrada aos dados de frota de
                    veículos por município disponíbilizados pelo Ministério dos Transportes.
                </p>
            </article>
            """
        )

    with col_objetivo:
        st.html(
            """
            <article class="about-card">
                <p class="about-card-label">02</p>
                <h3 class="about-card-title">Objetivo</h3>
                <p class="about-card-text">
                    Estimar a probabilidade de uma pessoa envolvida em um
                    acidente apresentar ficar em entado grave (lesões graves ou óbito).
                </p>
            </article>
            """
        )

    col_modelo, col_aplicacao = st.columns(2, gap="large")

    with col_modelo:
        st.html(
            """
            <article class="about-card">
                <p class="about-card-label">03</p>
                <h3 class="about-card-title">Modelo Preditivo</h3>
                <p class="about-card-text">
                    Modelo XGBoost otimizado e avaliado com dados históricos,
                    considerando características da via, do ambiente, do
                    veículo e do local do acidente.
                </p>
            </article>
            """
        )

    with col_aplicacao:
        st.html(
            """
            <article class="about-card">
                <p class="about-card-label">04</p>
                <h3 class="about-card-title">Aplicação</h3>
                <p class="about-card-text">
                    Ambiente interativo com exploração dos dados históricos,
                    simulação de novos cenários e interpretação das previsões
                    realizadas pelo modelo.
                </p>
            </article>
            """
        )