"""
dashboard_loader.py

Carrega e prepara os dados utilizados no Dashboard.
"""


import pandas as pd
import streamlit as st
import os

from huggingface_hub import hf_hub_download

HF_REPO_ID = "elainerreis/predicao_acidentes"
HF_DATA_FILENAME = "amostra_17-25.csv"


@st.cache_data(show_spinner=False)
def load_dashboard_data():
    """
    Baixa a base do Dashboard do Hugging Face.
    """

    token = os.getenv("HF_TOKEN")

    csv_path = hf_hub_download(
        repo_id=HF_REPO_ID,
        filename=HF_DATA_FILENAME,
        repo_type="model",
        token=token,
    )

    df = pd.read_csv(csv_path)

    print(f"Linhas carregadas: {len(df):,}")

    if "ano" in df.columns:
        df["ano"] = df["ano"].astype(int)

    if "br" in df.columns:
        df["br"] = df["br"].astype(str)

    if "km" in df.columns:
        df["km"] = pd.to_numeric(
            df["km"],
            errors="coerce",
        )

    if "frota" in df.columns:
        df["frota"] = pd.to_numeric(
            df["frota"],
            errors="coerce",
        )

    if "gravidade" in df.columns:
        df["gravidade"] = (
            pd.to_numeric(
                df["gravidade"],
                errors="coerce",
            )
            .fillna(0)
            .astype(int)
        )

    return df