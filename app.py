"""
app.py

Ponto de entrada e controlador de navegação da aplicação.
"""

import streamlit as st
from components.styles import apply_styles
from config import (
    PAGE_TITLE,
    PAGE_ICON,
    LAYOUT,
)


# ======================================================
# CONFIGURAÇÃO GLOBAL
# ======================================================

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded",
)

apply_styles()
# ======================================================
# DEFINIÇÃO DAS PÁGINAS
# ======================================================

pagina_inicio = st.Page(
    "pages/home.py",
    title="Início",
    icon=":material/home:",
    default=True,
)

pagina_dashboard = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon=":material/analytics:",
)

pagina_predicao = st.Page(
    "pages/predict.py",
    title="Predição",
    icon=":material/target:",
)


# ======================================================
# NAVEGAÇÃO
# ======================================================

navegacao = st.navigation(
    [
        pagina_inicio,
        pagina_dashboard,
        pagina_predicao,
    ],
    position="sidebar",
    expanded=True,
)

navegacao.run()