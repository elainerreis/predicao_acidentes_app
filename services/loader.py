"""
loader.py

Centraliza o carregamento dos artefatos utilizados pela aplicação.
Cada artefato é carregado somente quando solicitado.
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

MODEL_PATH = MODELS_DIR / "modelo_xgboost_final.ubj"
METADATA_PATH = MODELS_DIR / "metadata.pkl"
SPLITS_PATH = MODELS_DIR / "data_splits.pkl"
SHAP_PATH = MODELS_DIR / "shap_values_cache.pkl"


# ======================================================
# MODELO
# ======================================================

@st.cache_resource(show_spinner=False)
def load_model() -> XGBClassifier:
    """
    Carrega o modelo XGBoost salvo no formato nativo UBJSON.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modelo não encontrado em: {MODEL_PATH}"
        )

    model = XGBClassifier()
    model.load_model(MODEL_PATH)

    return model


# ======================================================
# METADADOS
# ======================================================

@st.cache_data(show_spinner=False)
def load_metadata() -> dict[str, Any]:
    """
    Carrega os metadados utilizados na construção das features
    e dos campos da página de predição.
    """

    if not METADATA_PATH.exists():
        raise FileNotFoundError(
            f"Metadata não encontrado em: {METADATA_PATH}"
        )

    metadata = joblib.load(METADATA_PATH)

    if not isinstance(metadata, dict):
        raise TypeError(
            "O arquivo metadata.pkl deve conter um dicionário."
        )

    return metadata


# ======================================================
# ARTEFATOS DA PREDIÇÃO
# ======================================================

@st.cache_resource(show_spinner=False)
def load_artifacts() -> dict[str, Any]:
    """
    Retorna o modelo e os metadados utilizados pela página
    de predição.
    """

    return {
        "model": load_model(),
        **load_metadata(),
    }


# ======================================================
# EXPLICADOR SHAP INDIVIDUAL
# ======================================================

@st.cache_resource(show_spinner=False)
def load_explainer() -> shap.TreeExplainer:
    """
    Cria o explicador SHAP somente quando solicitado.
    """

    return shap.TreeExplainer(load_model())


# ======================================================
# DADOS DE AVALIAÇÃO
# ======================================================

@st.cache_resource(show_spinner=False)
def load_evaluation_data():
    """
    Carrega os conjuntos de treino e teste.

    Essa função deve ser utilizada apenas nas páginas que
    realmente precisam desses dados.
    """

    if not SPLITS_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo de splits não encontrado em: {SPLITS_PATH}"
        )

    X_train, X_test, y_train, y_test = joblib.load(SPLITS_PATH)

    return X_train, X_test, y_train, y_test


# ======================================================
# SHAP GLOBAL
# ======================================================

@st.cache_resource(show_spinner=False)
def load_global_shap():
    """
    Carrega os valores SHAP globais previamente calculados.
    """

    if not SHAP_PATH.exists():
        raise FileNotFoundError(
            f"Cache SHAP não encontrado em: {SHAP_PATH}"
        )

    return joblib.load(SHAP_PATH)


# ======================================================
# ARTEFATOS DA HOME / ANÁLISE GLOBAL
# ======================================================

def load_global_analysis_artifacts():
    """
    Retorna os artefatos utilizados na análise global do modelo.
    """

    model = load_model()
    X_train, X_test, y_train, y_test = load_evaluation_data()
    shap_values = load_global_shap()

    return (
        model,
        X_train,
        X_test,
        y_train,
        y_test,
        shap_values,
    )