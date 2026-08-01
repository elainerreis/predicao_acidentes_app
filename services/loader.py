"""
loader.py

Carrega os artefatos necessários para a predição.
"""

from pathlib import Path
from typing import Any

import joblib
import shap
import streamlit as st
from xgboost import XGBClassifier


# ======================================================
# CAMINHOS
# ======================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT_DIR / "models"

MODEL_PATH = (
    MODELS_DIR
    / "modelo_xgboost_final.ubj"
)

METADATA_PATH = (
    MODELS_DIR
    / "metadata.pkl"
)


# ======================================================
# MODELO E METADATA
# ======================================================

@st.cache_resource(show_spinner=False)
def load_artifacts() -> dict[str, Any]:
    """
    Carrega o modelo e os metadados utilizados
    na página de predição.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modelo não encontrado: {MODEL_PATH}"
        )

    if not METADATA_PATH.exists():
        raise FileNotFoundError(
            f"Metadata não encontrado: {METADATA_PATH}"
        )

    model = XGBClassifier()

    model.load_model(
        MODEL_PATH
    )

    metadata = joblib.load(
        METADATA_PATH
    )

    if not isinstance(metadata, dict):
        raise TypeError(
            "O arquivo metadata.pkl deve conter "
            "um dicionário."
        )

    return {
        "model": model,
        **metadata,
    }


# ======================================================
# EXPLICADOR SHAP LOCAL
# ======================================================

@st.cache_resource(show_spinner=False)
def load_explainer() -> shap.TreeExplainer:
    """
    Cria o explicador SHAP apenas quando uma
    previsão individual precisar ser explicada.
    """

    artifacts = load_artifacts()

    return shap.TreeExplainer(
        artifacts["model"]
    )