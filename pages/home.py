"""
home.py

Página inicial da aplicação.
"""

from pathlib import Path

import streamlit as st

from components.home_hero import show_hero
from components.home_cards import show_project_cards
from components.home_workflow import show_workflow
from components.home_features import show_features
from components.home_model_metrics import show_model_metrics
from components.home_model_global_shap import (
    show_global_shap,
    show_global_shap_analysis,
)


# ======================================================
# CAMINHO DA IMAGEM SHAP
# ======================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

GLOBAL_SHAP_IMAGE_PATH = (
    ROOT_DIR
    / "assets"
    / "images"
    / "shap_global.png"
)


# ======================================================
# HERO
# ======================================================

show_hero()

st.divider()


# ======================================================
# PROJETO
# ======================================================

show_project_cards()

st.divider()


# ======================================================
# FLUXO
# ======================================================

show_workflow()

st.divider()


# ======================================================
# FUNCIONALIDADES
# ======================================================

show_features()

st.divider()


# ======================================================
# MÉTRICAS
# ======================================================

show_model_metrics()

st.divider()


# ======================================================
# SHAP GLOBAL
# ======================================================

st.header("Interpretabilidade do Modelo")

if GLOBAL_SHAP_IMAGE_PATH.exists():

    show_global_shap(
        GLOBAL_SHAP_IMAGE_PATH
    )

else:

    st.warning(
        "A imagem do SHAP global não foi encontrada."
    )

st.caption(
    """
    O gráfico apresenta a importância média absoluta dos valores SHAP.
    Quanto maior a barra, maior foi a contribuição média da variável
    para as previsões realizadas pelo modelo.
    """
)

show_global_shap_analysis()