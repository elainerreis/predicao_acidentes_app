"""
gerar_imagem_shap_global.py

Gera uma imagem estática da importância global das
variáveis utilizando o cache SHAP já calculado.
"""

from pathlib import Path
import copy

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap


ROOT_DIR = Path(__file__).resolve().parent.parent

SHAP_CACHE_PATH = (
    ROOT_DIR
    / "models"
    / "shap_values_cache.pkl"
)

OUTPUT_DIR = (
    ROOT_DIR
    / "assets"
    / "images"
)

OUTPUT_PATH = (
    OUTPUT_DIR
    / "shap_global.png"
)


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


NOMES_VARIAVEIS = {
    "uf": "Estado (UF)",
    "br": "Rodovia (BR)",
    "br_km": "Trecho (BR + KM)",
    "dia_semana": "Dia da semana",
    "fase_dia": "Fase do dia",
    "sentido_via": "Sentido da via",
    "condicao_metereologica": "Condição meteorológica",
    "condicao_meteorologica": "Condição meteorológica",
    "tipo_pista": "Tipo de pista",
    "uso_solo": "Perímetro urbano",
    "tipo_veiculo": "Tipo de veículo",
    "ano": "Ano",
    "frota": "Frota municipal",
    "tracado_via": "Traçado da via",
}


def agrupar_tracado(
    shap_values: shap.Explanation,
) -> shap.Explanation:
    """
    Agrupa as variáveis binárias de traçado da via
    em uma única variável global.
    """

    shap_values = copy.deepcopy(
        shap_values
    )

    valores = np.asarray(
        shap_values.values
    ).copy()

    dados = (
        np.asarray(
            shap_values.data
        ).copy()
        if shap_values.data is not None
        else None
    )

    nomes = list(
        shap_values.feature_names
    )

    indices = [
        indice
        for indice, nome in enumerate(nomes)
        if str(nome) in TRACADOS
    ]

    if len(indices) <= 1:
        return shap_values

    indice_mestre = indices[0]
    indices_remover = indices[1:]

    valores[:, indice_mestre] = (
        valores[:, indices].sum(axis=1)
    )

    if dados is not None:
        dados[:, indice_mestre] = (
            dados[:, indices].sum(axis=1)
        )

    nomes[indice_mestre] = "tracado_via"

    valores = np.delete(
        valores,
        indices_remover,
        axis=1,
    )

    if dados is not None:
        dados = np.delete(
            dados,
            indices_remover,
            axis=1,
        )

    nomes = [
        nome
        for indice, nome in enumerate(nomes)
        if indice not in indices_remover
    ]

    return shap.Explanation(
        values=valores,
        data=dados,
        feature_names=nomes,
        base_values=shap_values.base_values,
    )


def criar_dataframe_importancia(
    shap_values: shap.Explanation,
) -> pd.DataFrame:
    """
    Calcula a importância média absoluta das variáveis.
    """

    shap_agrupado = agrupar_tracado(
        shap_values
    )

    impactos = np.abs(
        np.asarray(shap_agrupado.values)
    ).mean(axis=0)

    nomes = [
        NOMES_VARIAVEIS.get(
            str(nome),
            str(nome),
        )
        for nome in shap_agrupado.feature_names
    ]

    dataframe = pd.DataFrame(
        {
            "Variável": nomes,
            "Impacto": impactos,
        }
    )

    return dataframe.sort_values(
        by="Impacto",
        ascending=True,
    )


def criar_grafico(
    dataframe: pd.DataFrame,
) -> None:
    """
    Gera e salva o gráfico como PNG.
    """

    altura = max(
        7,
        len(dataframe) * 0.42,
    )

    fig, ax = plt.subplots(
        figsize=(12, altura)
    )

    barras = ax.barh(
        dataframe["Variável"],
        dataframe["Impacto"],
    )

    maior_impacto = float(
        dataframe["Impacto"].max()
    )

    margem_texto = (
        maior_impacto * 0.015
        if maior_impacto > 0
        else 0.01
    )

    for barra, valor in zip(
        barras,
        dataframe["Impacto"],
    ):
        ax.text(
            valor + margem_texto,
            barra.get_y()
            + barra.get_height() / 2,
            f"{valor:.2f}".replace(".", ","),
            va="center",
            fontsize=9,
        )

    ax.set_title(
        "Importância Global das Variáveis (SHAP)",
        fontsize=16,
        fontweight="bold",
        pad=18,
    )

    ax.set_xlabel(
        "Impacto médio absoluto (|SHAP|)",
        fontsize=11,
    )

    ax.set_ylabel("")

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.25,
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.set_xlim(
        0,
        maior_impacto * 1.16,
    )

    plt.tight_layout()

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig.savefig(
        OUTPUT_PATH,
        dpi=180,
        bbox_inches="tight",
        facecolor="white",
    )

    plt.close(fig)


def main() -> None:
    if not SHAP_CACHE_PATH.exists():
        raise FileNotFoundError(
            "Cache SHAP não encontrado em: "
            f"{SHAP_CACHE_PATH}"
        )

    print("Carregando o cache SHAP...")

    shap_values = joblib.load(
        SHAP_CACHE_PATH
    )

    print("Calculando importância global...")

    dataframe = criar_dataframe_importancia(
        shap_values
    )

    print(dataframe.sort_values(
        "Impacto",
        ascending=False,
    ).head(10))

    criar_grafico(dataframe)

    tamanho_mb = (
        OUTPUT_PATH.stat().st_size
        / (1024 ** 2)
    )

    print("\nImagem criada com sucesso.")
    print(f"Arquivo: {OUTPUT_PATH}")
    print(f"Tamanho: {tamanho_mb:.2f} MB")


if __name__ == "__main__":
    main()