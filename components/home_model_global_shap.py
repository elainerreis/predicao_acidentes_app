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

O gráfico apresenta a importância global das variáveis estimada pelo 
SHAP (SHapley Additive exPlanations), considerando o impacto 
médio absoluto de cada atributo nas previsões do modelo.
Assim, ele indica o quanto cada variável influencia as decisões do modelo, 
mas não se essa influência aumenta ou reduz a probabilidade de um acidente grave. 
A direção do impacto pode ser observada nas explicações individuais da página de predição.

Observa-se que o **Tipo de veículo** é a variável de maior impacto, 
seguido pelo **Trecho (BR + KM)**, **Frota municipal** e 
**Rodovia (BR)**. Esses resultados sugerem que tanto as características do 
veículo quanto o contexto geográfico e a infraestrutura da via desempenham 
papel relevante na estimativa da gravidade dos acidentes.
"""
    )