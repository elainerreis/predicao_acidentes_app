"""
loader.py

Carrega o modelo do Hugging Face Hub
e os metadados utilizados na predição.
"""

import os
from typing import Any

import joblib
import streamlit as st
from huggingface_hub import hf_hub_download
from xgboost import XGBClassifier


HF_REPO_ID = "elainerreis/predicao_acidentes"
HF_MODEL_FILENAME = "amostra_modelo_xgboost_final.ubj"
HF_METADATA_FILENAME = "amostra_metadata.pkl"


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
    Baixa o metadata do Hugging Face.
    """

    token = os.getenv("HF_TOKEN")

    metadata_path = hf_hub_download(
        repo_id=HF_REPO_ID,
        filename=HF_METADATA_FILENAME,
        repo_type="model",
        token=token,
    )

    metadata = joblib.load(metadata_path)

    if not isinstance(metadata, dict):
        raise TypeError(
            "O arquivo metadata deve conter um dicionário."
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