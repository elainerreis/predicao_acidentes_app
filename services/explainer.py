"""
explainer.py

Calcula contribuições SHAP utilizando
a implementação nativa do XGBoost.
"""

from typing import Any

import numpy as np
import pandas as pd
import xgboost as xgb


class LocalExplanation:
    """
    Estrutura mínima compatível com os componentes
    atuais de interpretação e plotagem.
    """

    def __init__(
        self,
        values: np.ndarray,
        data: np.ndarray,
        feature_names: list[str],
        base_values: np.ndarray,
    ) -> None:
        self.values = values
        self.data = data
        self.feature_names = feature_names
        self.base_values = base_values


def explain_prediction(
    model: Any,
    X: pd.DataFrame,
) -> LocalExplanation:
    """
    Calcula as contribuições SHAP de uma única
    observação diretamente pelo Booster do XGBoost.
    """

    if X.empty:
        raise ValueError(
            "O DataFrame de entrada está vazio."
        )

    booster = model.get_booster()

    dmatrix = xgb.DMatrix(
        X,
        enable_categorical=True,
        feature_names=list(X.columns),
    )

    contribuicoes = booster.predict(
        dmatrix,
        pred_contribs=True,
        validate_features=True,
    )

    contribuicoes = np.asarray(
        contribuicoes
    )

    if contribuicoes.ndim != 2:
        raise ValueError(
            "Formato inesperado das contribuições "
            "retornadas pelo XGBoost."
        )

    # A última coluna é o valor-base/bias.
    valores_shap = contribuicoes[:, :-1]

    valores_base = contribuicoes[:, -1]

    return LocalExplanation(
        values=valores_shap,
        data=X.to_numpy(),
        feature_names=list(X.columns),
        base_values=valores_base,
    )