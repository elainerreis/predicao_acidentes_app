"""
converter_modelo.py

Converte o modelo XGBoost salvo em joblib/pickle
para o formato nativo UBJSON do XGBoost.

Não realiza novo treinamento.
"""

from pathlib import Path
import gc
import joblib
from xgboost import XGBClassifier


ROOT_DIR = Path(__file__).resolve().parent

MODELS_DIR = ROOT_DIR / "models"

MODELO_PKL_PATH = (
    MODELS_DIR
    / "modelo_xgboost_final.pkl"
)

MODELO_UBJ_PATH = (
    MODELS_DIR
    / "modelo_xgboost_final.ubj"
)


def tamanho_mb(caminho: Path) -> float:
    """Retorna o tamanho do arquivo em megabytes."""

    return caminho.stat().st_size / (1024 ** 2)


def main() -> None:
    if not MODELO_PKL_PATH.exists():
        raise FileNotFoundError(
            f"Modelo não encontrado: {MODELO_PKL_PATH}"
        )

    print("Carregando o modelo original...")
    print(
        f"Tamanho original: "
        f"{tamanho_mb(MODELO_PKL_PATH):.2f} MB"
    )

    modelo = joblib.load(
        MODELO_PKL_PATH
    )

    if not isinstance(modelo, XGBClassifier):
        raise TypeError(
            "O arquivo carregado não contém um "
            "XGBClassifier."
        )

    print("Salvando no formato UBJSON...")

    modelo.save_model(
        MODELO_UBJ_PATH
    )

    del modelo
    gc.collect()

    if not MODELO_UBJ_PATH.exists():
        raise RuntimeError(
            "O arquivo UBJSON não foi criado."
        )

    tamanho_original = tamanho_mb(
        MODELO_PKL_PATH
    )

    tamanho_novo = tamanho_mb(
        MODELO_UBJ_PATH
    )

    reducao = (
        1 - tamanho_novo / tamanho_original
    ) * 100

    print("\nConversão concluída.")
    print(
        f"Modelo original: "
        f"{tamanho_original:.2f} MB"
    )
    print(
        f"Modelo UBJSON: "
        f"{tamanho_novo:.2f} MB"
    )
    print(
        f"Redução: {reducao:.2f}%"
    )
    print(
        f"Novo arquivo: {MODELO_UBJ_PATH}"
    )


if __name__ == "__main__":
    main()