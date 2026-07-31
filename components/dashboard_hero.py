import streamlit as st


def show_dashboard_hero() -> None:

    st.html(
        """
        <section class="hero-section">
            <div class="hero-content">

                <p class="hero-eyebrow">
                    EXPLORAÇÃO DOS DADOS
                </p>

                <h1 class="hero-title">
                    Análise Exploratória dos Acidentes Rodoviários
                </h1>

                <p class="hero-subtitle">
                    Explore padrões presentes nos registros históricos
                </p>

                <p class="hero-description">
                    Utilize os filtros para investigar como fatores
                    espaciais, temporais, ambientais e operacionais
                    influenciam a distribuição dos acidentes registrados
                    nas rodovias federais brasileiras.
                </p>

                <div class="hero-indicators">

                    <div class="hero-indicator">
                        <span class="hero-indicator-value">
                            Filtros Dinâmicos
                        </span>

                        <span class="hero-indicator-label">
                            Análise personalizada
                        </span>
                    </div>

                    <div class="hero-indicator">
                        <span class="hero-indicator-value">
                            Visualizações Interativas
                        </span>

                        <span class="hero-indicator-label">
                            Distribuições e relações
                        </span>
                    </div>

                    <div class="hero-indicator">
                        <span class="hero-indicator-value">
                            Estatísticas Descritivas
                        </span>

                        <span class="hero-indicator-label">
                            Exploração dos dados históricos
                        </span>
                    </div>

                </div>

            </div>
        </section>
        """
    )