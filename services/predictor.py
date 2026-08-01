"""
predictor.py

Executa a predição do cenário informado.
"""

from services.loader import load_artifacts
from services.feature_engineering import build_features


def predict(dados: dict) -> dict:
    """
    Realiza a predição sem calcular SHAP.
    Este modo pode ser usado para diagnosticar
    o consumo de memória no Streamlit Cloud.
    """

    print("1. Carregando artefatos")

    artifacts = load_artifacts()

    print("2. Artefatos carregados")

    X = build_features(
        dados,
        artifacts,
    )

    print("3. Features construídas")
    print(X.shape)

    model = artifacts["model"]

    print("4. Iniciando predict_proba")

    probabilidade = float(
        model.predict_proba(X)[0][1]
    )

    print("5. predict_proba concluído")

    classe = int(
        model.predict(X)[0]
    )

    print("6. Predição concluída")

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
        "explanation": None,
        "dados_entrada": dados,
    }