"""
home_model_global_shap.py

Exibe a imagem estática do SHAP global.
"""

from pathlib import Path

import streamlit as st


def show_global_shap(
    image_path: Path,
) -> None:
    """
    Exibe a imagem pré-calculada da importância global SHAP.
    """

    st.image(
        str(image_path),
        width="stretch",
    )


def show_global_shap_analysis() -> None:
    """
    Exibe uma orientação textual para interpretação
    do gráfico SHAP global.
    """

    st.markdown(
        """
### Como interpretar o gráfico

O gráfico apresenta a importância global das variáveis por meio da
média dos valores absolutos de SHAP.

Variáveis com barras maiores tiveram maior participação média nas
decisões do modelo. Essa visualização representa a magnitude da
influência, mas não informa isoladamente se cada variável aumentou
ou reduziu a probabilidade estimada.

Os resultados representam associações aprendidas pelo modelo a partir
dos registros históricos e não devem ser interpretados como relações
diretas de causa e efeito.
"""
    )