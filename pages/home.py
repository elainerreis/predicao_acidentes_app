"""
home.py

Página inicial da aplicação.
"""

import streamlit as st

from services.loader import load_global_analysis_artifacts

from components.home_hero import show_hero
from components.home_cards import show_project_cards
from components.home_workflow import show_workflow
from components.home_features import show_features

from components.home_model_metrics import (
    calculate_metrics,
    show_metrics,
)

from components.home_model_global_shap import (
    show_global_shap,
    show_global_shap_analysis,
)


# ======================================================
# CARREGAMENTO DO MODELO
# ======================================================

(
    model,
    X_train,
    X_test,
    y_train,
    y_test,
    shap_values,
) = load_global_analysis_artifacts()

metrics = calculate_metrics(
    model,
    X_train,
    X_test,
    y_test,
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

st.header("Desempenho do Modelo")

show_metrics(metrics)

st.caption(
    """
As métricas apresentadas foram calculadas utilizando o conjunto de teste,
permitindo avaliar a capacidade de generalização do modelo.
"""
)

st.divider()

# ======================================================
# SHAP GLOBAL
# ======================================================

st.header("Interpretabilidade do Modelo")

show_global_shap(
    shap_values
)

st.caption(
    """
O gráfico apresenta a importância média absoluta (|SHAP|)
das variáveis utilizadas pelo modelo.

Quanto maior o valor, maior é a contribuição daquela variável
para as previsões realizadas pelo algoritmo.
"""
)

show_global_shap_analysis(
    shap_values,
    quantidade_variaveis=5,
)