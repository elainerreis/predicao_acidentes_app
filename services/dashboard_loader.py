"""
dashboard_loader.py

Carrega e prepara os dados utilizados no Dashboard.
"""

from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "amostra_17-25.csv"


@st.cache_data(show_spinner=False)
def load_dashboard_data():
    """
    Carrega a base utilizada pelo Dashboard.
    """

    df = pd.read_csv(DATA_PATH)
    print(f"Linhas carregadas: {len(df):,}")

    # -----------------------------
    # Ajustes de tipos
    # -----------------------------

    if "ano" in df.columns:
        df["ano"] = df["ano"].astype(int)

    if "br" in df.columns:
        df["br"] = df["br"].astype(str)

    if "km" in df.columns:
        df["km"] = pd.to_numeric(df["km"], errors="coerce")

    if "frota" in df.columns:
        df["frota"] = pd.to_numeric(df["frota"], errors="coerce")

    if "gravidade" in df.columns:
        df["gravidade"] = (
            pd.to_numeric(df["gravidade"], errors="coerce")
            .fillna(0)
            .astype(int)
        )

    return df