"""
loader.py

Carrega os artefatos necessários para a predição.

O modelo XGBoost é obtido do Hugging Face Hub.
O metadata permanece armazenado localmente no
repositório da aplicação.
"""

import os
from pathlib import Path
from typing import Any

import joblib
import shap
import streamlit as st
from huggingface_hub import hf_hub_download
from xgboost import XGBClassifier


# ======================================================
# CAMINHOS E CONFIGURAÇÕES
# ======================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT_DIR / "models"

# Repositório do modelo no Hugging Face.
HF_REPO_ID = "elainerreis/predicao_acidentes"

# Nome exato do arquivo dentro do repositório.
HF_MODEL_FILENAME = "amostra_modelo_xgboost_final.ubj"

# Tipo padrão de repositório do Hugging Face.
HF_REPO_TYPE = "model"

# Metadata mantido no repositório GitHub da aplicação.
METADATA_PATH = MODELS_DIR / "amostra_metadata.pkl"


# ======================================================
# DOWNLOAD DO MODELO
# ======================================================

@st.cache_resource(show_spinner=False)
def get_model_path() -> Path:
    """
    Baixa o modelo do Hugging Face Hub e retorna
    o caminho local do arquivo armazenado em cache.

    Caso o arquivo já esteja no cache do Hugging Face,
    ele não será baixado novamente.
    """

    token = os.getenv("HF_TOKEN")

    try:
        model_path = hf_hub_download(
            repo_id=HF_REPO_ID,
            filename=HF_MODEL_FILENAME,
            repo_type=HF_REPO_TYPE,
            revision="main",
            token=token,
        )

    except Exception as error:
        raise RuntimeError(
            "Não foi possível baixar o modelo do "
            "Hugging Face Hub. Verifique o nome do "
            "repositório, o nome do arquivo e a conexão "
            "com a internet."
        ) from error

    return Path(model_path)


# ======================================================
# CARREGAMENTO DO MODELO
# ======================================================

@st.cache_resource(show_spinner=False)
def load_model() -> XGBClassifier:
    """
    Carrega o modelo XGBoost a partir do arquivo
    obtido do Hugging Face Hub.
    """

    model_path = get_model_path()

    if not model_path.exists():
        raise FileNotFoundError(
            f"Modelo não encontrado no cache: {model_path}"
        )

    model = XGBClassifier()

    model.load_model(
        str(model_path)
    )

    return model


# ======================================================
# CARREGAMENTO DO METADATA
# ======================================================

@st.cache_resource(show_spinner=False)
def load_metadata() -> dict[str, Any]:
    """
    Carrega os metadados armazenados localmente.
    """

    if not METADATA_PATH.exists():
        raise FileNotFoundError(
            f"Metadata não encontrado: {METADATA_PATH}"
        )

    metadata = joblib.load(
        METADATA_PATH
    )

    if not isinstance(metadata, dict):
        raise TypeError(
            "O arquivo metadata.pkl deve conter "
            "um dicionário."
        )

    return metadata


# ======================================================
# ARTEFATOS DA PREDIÇÃO
# ======================================================

@st.cache_resource(show_spinner=False)
def load_artifacts() -> dict[str, Any]:
    """
    Retorna o modelo e os metadados necessários
    para construir e executar uma predição.
    """

    model = load_model()
    metadata = load_metadata()

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
    Cria o explicador SHAP uma única vez e o mantém
    em cache para as previsões seguintes.
    """

    model = load_model()

    return shap.TreeExplainer(
        model
    )