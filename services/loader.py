"""
loader.py

Carrega o modelo do Hugging Face Hub
e os metadados utilizados na predição.
"""

import os
from pathlib import Path
from typing import Any

import joblib
import streamlit as st
from huggingface_hub import hf_hub_download
from xgboost import XGBClassifier


ROOT_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT_DIR / "models"

HF_REPO_ID = "elainerreis/predicao_acidentes"
HF_MODEL_FILENAME = "amostra_modelo_xgboost_final.ubj"

METADATA_PATH = MODELS_DIR / "amostra_metadata.pkl"


@st.cache_resource(
    show_spinner="Carregando o modelo de predição..."
)
def load_model() -> XGBClassifier:
    """
    Baixa o modelo do Hugging Face Hub e o mantém
    em cache após o primeiro carregamento.
    """

    token = os.getenv("HF_TOKEN")

    model_path = hf_hub_download(
        repo_id=HF_REPO_ID,
        filename=HF_MODEL_FILENAME,
        repo_type="model",
        token=token,
    )

    model = XGBClassifier()

    model.load_model(
        model_path
    )

    return model


@st.cache_resource(show_spinner=False)
def load_metadata() -> dict[str, Any]:
    """
    Carrega os metadados usados para preparar
    os dados da predição.
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


@st.cache_resource(show_spinner=False)
def load_artifacts() -> dict[str, Any]:
    """
    Retorna o modelo e os metadados necessários
    para a predição.
    """

    return {
        "model": load_model(),
        **load_metadata(),
    }