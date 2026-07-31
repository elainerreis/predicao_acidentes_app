"""
predictor.py

Executa a predição e retorna os resultados utilizados
na apresentação e na interpretação do cenário.
"""

from services.loader import (
    load_artifacts,
    load_explainer,
)

from services.feature_engineering import build_features
from services.explainer import explain_prediction


def predict(
    dados: dict,
    gerar_explicacao: bool = True,
) -> dict:
    """
    Realiza a predição da gravidade para o cenário informado.

    Parameters
    ----------
    dados:
        Dados preenchidos pelo usuário.

    gerar_explicacao:
        Quando True, calcula a explicação SHAP.
        Quando False, realiza apenas a predição.
    """

    artifacts = load_artifacts()

    X = build_features(
        dados,
        artifacts,
    )

    model = artifacts["model"]

    probabilidade = float(
        model.predict_proba(X)[0][1]
    )

    classe = int(
        model.predict(X)[0]
    )

    explanation = None

    if gerar_explicacao:
        explainer = load_explainer()

        explanation = explain_prediction(
            explainer,
            X,
        )

    return {
        "classe": classe,
        "probabilidade": probabilidade,
        "percentual": round(
            probabilidade * 100,
            2,
        ),
        "risco": (
            "Grave"
            if classe == 1
            else "Não Grave"
        ),
        "features": X,
        "explanation": explanation,
        "dados_entrada": dados,
    }