"""
predictor.py

Executa a predição e calcula as contribuições
locais utilizando o XGBoost.
"""

from services.loader import load_artifacts
from services.feature_engineering import build_features
from services.explainer import explain_prediction


def predict(
    dados: dict,
) -> dict:
    """
    Realiza a predição e gera a explicação local.
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
        probabilidade >= 0.5
    )

    explanation = explain_prediction(
        model,
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