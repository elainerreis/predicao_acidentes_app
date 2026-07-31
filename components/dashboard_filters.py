"""
dashboard_filters.py

Filtros globais do Dashboard.
"""

import pandas as pd
import streamlit as st


def show_filters(df):
    """
    Exibe filtros inteligentes em cascata.
    """

    st.sidebar.header("Filtros")

    # ---------------------------------------------------
    # Padronização dos tipos
    # ---------------------------------------------------

    df = df.copy()

    NA_LABEL = "Não informado"

    df["ano"] = pd.to_numeric(
        df["ano"],
        errors="coerce",
    ).astype("Int64")

    df["uf"] = (
        df["uf"]
        .fillna(NA_LABEL)
        .astype(str)
        .str.strip()
    )

    df["br"] = (
        df["br"]
        .fillna(NA_LABEL)
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.strip()
    )

    df["tipo_veiculo"] = (
        df["tipo_veiculo"]
        .fillna(NA_LABEL)
        .astype(str)
        .str.strip()
    )

    df["gravidade"] = (
        pd.to_numeric(
            df["gravidade"],
            errors="coerce",
        )
        .fillna(0)
        .astype(int)
    )

    # ---------------------------------------------------
    # ANO
    # ---------------------------------------------------

    anos = sorted(
        df["ano"]
        .dropna()
        .unique()
        .tolist()
    )

    anos_sel = st.sidebar.multiselect(
        "Ano",
        anos,
        default=anos,
    )

    df1 = df[df["ano"].isin(anos_sel)]

    # ---------------------------------------------------
    # UF
    # ---------------------------------------------------

    ufs = (
        df1["uf"]
        .sort_values()
        .unique()
        .tolist()
    )

    ufs_sel = st.sidebar.multiselect(
        "UF",
        ufs,
        default=ufs,
    )

    df2 = df1[
        df1["uf"].isin(ufs_sel)
    ]

    # ---------------------------------------------------
    # BR
    # ---------------------------------------------------

    brs = (
        df2["br"]
        .sort_values()
        .unique()
        .tolist()
    )

    brs_sel = st.sidebar.multiselect(
        "BR",
        brs,
        default=brs,
    )

    df3 = df2[
        df2["br"].isin(brs_sel)
    ]

    # ---------------------------------------------------
    # Tipo de veículo
    # ---------------------------------------------------

    veiculos = (
        df3["tipo_veiculo"]
        .sort_values()
        .unique()
        .tolist()
    )

    veiculos_sel = st.sidebar.multiselect(
        "Tipo de veículo",
        veiculos,
        default=veiculos,
    )

    df4 = df3[
        df3["tipo_veiculo"].isin(
            veiculos_sel
        )
    ]

    # ---------------------------------------------------
    # Gravidade
    # ---------------------------------------------------

    gravidade = st.sidebar.radio(
        "Gravidade",
        [
            "Todos",
            "Grave",
            "Não Grave",
        ],
    )

    if gravidade == "Grave":

        df4 = df4[
            df4["gravidade"] == 1
        ]

    elif gravidade == "Não Grave":

        df4 = df4[
            df4["gravidade"] == 0
        ]

    return df4