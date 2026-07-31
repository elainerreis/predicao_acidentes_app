"""
dashboard.py

Página de Análise Exploratória dos Acidentes Rodoviários.
"""

import streamlit as st

from services.dashboard_loader import load_dashboard_data

from components.dashboard_hero import show_dashboard_hero
from components.dashboard_filters import show_filters
from components.dashboard_cards import show_dashboard_cards

from components.dashboard_bar import (
    show_location_charts,
    show_time_charts,
    show_conditions_charts,
    show_vehicle_chart,
)

from components.dashboard_heatmap import show_heatmaps
from components.dashboard_scatter import show_scatter_charts
from components.dashboard_analysis import (
    show_location_analysis,
    show_time_analysis,
    show_conditions_analysis,
    show_vehicle_analysis,
)

# ======================================================
# CARREGAMENTO DOS DADOS E FILTROS
# ======================================================

df = load_dashboard_data()

df = show_filters(df)


# ======================================================
# HERO
# ======================================================

show_dashboard_hero()
st.info(
    """
    **Sobre os dados**

    Para otimizar o desempenho da aplicação, este dashboard utiliza uma
    amostra aleatória de aproximadamente **10% da base utilizada para treinar o modelo**.
    Essa amostra é utilizada **apenas para exploração dos dados**.

    """
)
st.divider()


# ======================================================
# 1. VISÃO GERAL
# ======================================================

st.header("1. Visão Geral")

st.write(
    """
Os indicadores abaixo resumem o conjunto de dados atualmente
selecionado pelos filtros.
"""
)

show_dashboard_cards(df)

st.divider()


# ======================================================
# 2. LOCALIZAÇÃO
# ======================================================

st.header("2. Onde os acidentes ocorrem?")

st.write(
    """
Esta seção apresenta a distribuição espacial dos registros,
permitindo identificar estados e rodovias com maior concentração
de pessoas envolvidas em acidentes, além de comparar frequência
e taxa de gravidade entre as unidades da federação.
"""
)

st.markdown("#### Distribuição dos registros")

show_location_charts(df)

st.markdown("#### Frequência e taxa de gravidade por UF")

show_scatter_charts(df)

show_location_analysis(df)

st.divider()

# ======================================================
# 3. DISTRIBUIÇÃO TEMPORAL
# ======================================================

st.header("3. Quando os acidentes acontecem?")

st.write(
    """
Os gráficos apresentam a evolução dos registros ao longo dos anos
e sua distribuição entre os dias da semana e as diferentes fases
do dia.
"""
)

show_time_charts(df)

st.markdown("#### Relação entre dia da semana e fase do dia")

show_heatmaps(df)

show_time_analysis(df)

st.divider()


# ======================================================
# 4. CONDIÇÕES DA VIA E DO AMBIENTE
# ======================================================

st.header("4. Em quais condições os acidentes ocorrem?")

st.write(
    """
Esta seção apresenta características da via e do ambiente
associadas aos registros selecionados, incluindo o tipo de pista,
a condição meteorológica, o perímetro urbano e o traçado da via.
"""
)

show_conditions_charts(df)

show_conditions_analysis(df)

st.divider()

# ======================================================
# 5. PERFIL DOS VEÍCULOS ENVOLVIDOS
# ======================================================

st.header("5. Perfil dos veículos envolvidos")

st.write(
    """
Esta seção apresenta os tipos de veículo associados às pessoas
envolvidas nos registros selecionados.
"""
)

show_vehicle_chart(df)

show_vehicle_analysis(df)

st.divider()