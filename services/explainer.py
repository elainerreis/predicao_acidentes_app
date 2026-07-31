"""
explainer.py

Gera a explicação SHAP de uma previsão individual.
"""

import shap
import pandas as pd


def explain_prediction(
    explainer: shap.TreeExplainer,
    X: pd.DataFrame,
):
    """
    Calcula a explicação SHAP para uma observação.

    Parameters
    ----------
    explainer:
        Explicador SHAP já carregado.

    X:
        DataFrame com as features da observação.
    """

    explanation = explainer(X)

    return explanation