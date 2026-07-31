"""
feature_engineering.py

Responsável por transformar os dados informados pelo usuário
no mesmo formato utilizado durante o treinamento do modelo.

Não realiza predição.
"""

from typing import Dict

import pandas as pd


# ==========================================================
# NORMALIZAÇÃO
# ==========================================================

def normalizar_br(br) -> str:
    """
    O modelo foi treinado com a BR no formato:

    101.0
    116.0
    230.0
    """

    return f"{float(br):.1f}"


def normalizar_ano(ano) -> str:
    """
    Ano é tratado como variável categórica.
    """

    return str(ano)


def normalizar_categoria(valor: str, categorias: list) -> str:
    """
    Procura uma categoria ignorando maiúsculas,
    minúsculas e espaços.

    Exemplo

    "SÁBADO"

    →

    "sábado"
    """

    valor = str(valor).strip().casefold()

    for categoria in categorias:

        if str(categoria).strip().casefold() == valor:
            return categoria

    raise ValueError(
        f"\nValor '{valor}' não encontrado.\n"
        f"\nCategorias válidas:\n{categorias}"
    )


# ==========================================================
# TRAÇADO DA VIA
# ==========================================================

TRACADOS = [
    "Aclive",
    "Curva",
    "Declive",
    "Desvio Temporário",
    "Em Obras",
    "Interseção de Vias",
    "Ponte",
    "Reta",
    "Retorno Regulamentado",
    "Rotatória",
    "Túnel",
    "Viaduto",
]


def criar_dummies_tracado(tracados):

    dummies = {item: 0 for item in TRACADOS}

    for item in tracados:

        if item in dummies:
            dummies[item] = 1

    return dummies


# ==========================================================
# BR_KM
# ==========================================================

def criar_br_km(br, km):
    """
    Reproduz exatamente o formato aprendido pelo modelo.

    Exemplo

    BR = 230

    KM = 105

    →

    230.0105.0
    """

    br = f"{float(br):.1f}"

    km = f"{round(float(km),0):.1f}"

    return br + km


# ==========================================================
# FEATURE ENGINEERING
# ==========================================================

def build_features(
    dados: Dict,
    artifacts: Dict
) -> pd.DataFrame:

    registro = dados.copy()

    # ------------------------------------------------------
    # Conversões
    # ------------------------------------------------------

    registro["br"] = normalizar_br(registro["br"])

    registro["ano"] = normalizar_ano(registro["ano"])

    registro["uf"] = normalizar_categoria(
        registro["uf"],
        artifacts["categories"]["uf"],
    )

    registro["dia_semana"] = normalizar_categoria(
        registro["dia_semana"],
        artifacts["categories"]["dia_semana"],
    )

    registro["fase_dia"] = normalizar_categoria(
        registro["fase_dia"],
        artifacts["categories"]["fase_dia"],
    )

    registro["sentido_via"] = normalizar_categoria(
        registro["sentido_via"],
        artifacts["categories"]["sentido_via"],
    )

    registro["condicao_metereologica"] = normalizar_categoria(
        registro["condicao_metereologica"],
        artifacts["categories"]["condicao_metereologica"],
    )

    registro["tipo_pista"] = normalizar_categoria(
        registro["tipo_pista"],
        artifacts["categories"]["tipo_pista"],
    )

    registro["uso_solo"] = normalizar_categoria(
        registro["uso_solo"],
        artifacts["categories"]["uso_solo"],
    )

    registro["tipo_veiculo"] = normalizar_categoria(
        registro["tipo_veiculo"],
        artifacts["categories"]["tipo_veiculo"],
    )

    registro["frota"] = float(registro["frota"])

    # ------------------------------------------------------
    # BR_KM
    # ------------------------------------------------------

    registro["br_km"] = criar_br_km(
        registro["br"],
        registro["km"],
    )

    registro["br_km"] = normalizar_categoria(
        registro["br_km"],
        artifacts["categories"]["br_km"],
    )

    # ------------------------------------------------------
    # Traçado
    # ------------------------------------------------------

    tracados = registro.pop("tracado_via")

    registro.pop("km")

    registro.update(
        criar_dummies_tracado(tracados)
    )

    # ------------------------------------------------------
    # DataFrame
    # ------------------------------------------------------

    df = pd.DataFrame([registro])

    # ------------------------------------------------------
    # Garante todas as features
    # ------------------------------------------------------

    for coluna in artifacts["features"]:

        if coluna not in df.columns:
            df[coluna] = 0

    # ------------------------------------------------------
    # Ordem correta
    # ------------------------------------------------------

    df = df[artifacts["features"]]

    # ------------------------------------------------------
    # Conversão para category
    # ------------------------------------------------------

    for coluna in artifacts["categorical_columns"]:

        df[coluna] = pd.Categorical(
            df[coluna],
            categories=artifacts["categories"][coluna],
        )

    return df