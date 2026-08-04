"""
predict.py

Página destinada à simulação da gravidade de acidentes
em rodovias federais brasileiras.
"""

import streamlit as st

from services.loader import load_metadata
from services.predictor import predict
from components.predict_analysis import show_prediction
from components.prediction_form import show_prediction_form
from components.predict_hero import show_prediction_hero


metadata = load_metadata()

show_prediction_hero()

st.info(
    """
    Esta versão demonstrativa utiliza um modelo treinado com uma amostra
    de 10% dos dados disponíveis. Os resultados devem ser interpretados
    como uma prova de conceito.
    """
)

st.markdown("## Simulação do cenário")

st.markdown(
    """
Preencha os campos abaixo com as características do cenário que deseja
analisar. O resultado representa uma estimativa probabilística baseada
nos padrões identificados pelo modelo nos dados históricos.
"""
)

dados = show_prediction_form(metadata)

if dados is not None:
    with st.spinner("Processando o cenário informado..."):
        try:
            resultado = predict(dados)

        except Exception as error:
            st.error(
                """
                Não foi possível realizar a previsão. Verifique os dados
                informados e tente novamente.
                """
            )

            with st.expander("Detalhes técnicos do erro"):
                st.exception(error)

        else:
            st.divider()
            st.markdown("## Resultado da predição")
            show_prediction(resultado)