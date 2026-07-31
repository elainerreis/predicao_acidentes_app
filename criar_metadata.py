"""
criar_metadata.py

Gera apenas os metadados necessários para a aplicação.
"""

from pathlib import Path
import gc
import joblib
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parent

MODELS_DIR = ROOT_DIR / "models"

DATA_SPLITS_PATH = (
    MODELS_DIR
    / "data_splits.pkl"
)

METADATA_PATH = (
    MODELS_DIR
    / "metadata.pkl"
)


def extrair_km(
    br_km: object,
    br: object,
) -> float | None:
    """
    Extrai o valor do quilômetro da coluna br_km.

    Exemplo:
        br = "110.0"
        br_km = "110.040.0"
        km = 40.0
    """

    if pd.isna(br_km) or pd.isna(br):
        return None

    br_texto = str(br).strip()
    br_km_texto = str(br_km).strip()

    if not br_km_texto.startswith(
        br_texto
    ):
        return None

    km_texto = br_km_texto[
        len(br_texto):
    ].strip()

    if not km_texto:
        return None

    try:
        return float(km_texto)

    except (TypeError, ValueError):
        return None


def criar_limites_localizacao(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
) -> dict:
    """
    Retorna um dicionário no formato:

    {
        "UF": {
            "BR": km_maximo
        }
    }
    """

    localizacao = pd.concat(
        [
            X_train[
                ["uf", "br", "br_km"]
            ],
            X_test[
                ["uf", "br", "br_km"]
            ],
        ],
        ignore_index=True,
    )

    localizacao = localizacao.dropna(
        subset=["uf", "br", "br_km"]
    ).copy()

    localizacao["uf"] = (
        localizacao["uf"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    localizacao["br"] = (
        localizacao["br"]
        .astype(str)
        .str.strip()
    )

    localizacao["km"] = localizacao.apply(
        lambda linha: extrair_km(
            br_km=linha["br_km"],
            br=linha["br"],
        ),
        axis=1,
    )

    localizacao = localizacao.dropna(
        subset=["km"]
    )

    localizacao = localizacao.loc[
        localizacao["km"] >= 0
    ]

    limites = (
        localizacao
        .groupby(
            ["uf", "br"],
            as_index=False,
            observed=True,
        )["km"]
        .max()
    )

    location_limits = {}

    for linha in limites.itertuples(
        index=False
    ):
        location_limits.setdefault(
            str(linha.uf),
            {},
        )[str(linha.br)] = float(
            linha.km
        )

    return location_limits


def main() -> None:
    if not DATA_SPLITS_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: "
            f"{DATA_SPLITS_PATH}"
        )

    print("Carregando os dados de treino e teste...")

    X_train, X_test, _, _ = joblib.load(
        DATA_SPLITS_PATH
    )

    categorical_columns = list(
        X_train.select_dtypes(
            include=[
                "object",
                "category",
            ]
        ).columns
    )

    categories = {}

    for coluna in categorical_columns:
        categories[coluna] = sorted(
            X_train[coluna]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    location_limits = (
        criar_limites_localizacao(
            X_train,
            X_test,
        )
    )

    metadata = {
        "features": list(
            X_train.columns
        ),
        "categorical_columns": (
            categorical_columns
        ),
        "categories": categories,
        "dtypes": {
            coluna: str(dtype)
            for coluna, dtype
            in X_train.dtypes.items()
        },
        "location_limits": (
            location_limits
        ),
        "days_order": [
            "segunda-feira",
            "terça-feira",
            "quarta-feira",
            "quinta-feira",
            "sexta-feira",
            "sábado",
            "domingo",
        ],
    }

    joblib.dump(
        metadata,
        METADATA_PATH,
        compress=3,
    )

    del X_train
    del X_test
    gc.collect()

    tamanho_mb = (
        METADATA_PATH.stat().st_size
        / (1024 ** 2)
    )

    print("Metadata criado com sucesso.")
    print(
        f"Tamanho: {tamanho_mb:.2f} MB"
    )
    print(
        f"UFs: {len(location_limits)}"
    )
    print(
        "Combinações UF/BR:",
        sum(
            len(brs)
            for brs
            in location_limits.values()
        ),
    )


if __name__ == "__main__":
    main()