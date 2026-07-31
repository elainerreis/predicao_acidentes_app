"""
predict.py

Página destinada à simulação da gravidade de acidentes
em rodovias federais brasileiras.
"""

import streamlit as st

from config import FIELDS, OPTIONS, TRACADOS
from services.predictor import predict
from components.predict_analysis import show_prediction
from components.predict_hero import show_prediction_hero

# =========================================================
# =========================================================
# HERO
# =========================================================

show_prediction_hero()

st.markdown("## Simulação do cenário")

st.markdown(
    """
Preencha os campos abaixo com as características do cenário que deseja
analisar. O resultado representa uma estimativa probabilística baseada
nos padrões identificados pelo modelo nos dados históricos.
"""
)


# =========================================================
# FORMULÁRIO DE PREDIÇÃO
# =========================================================

with st.form("prediction_form"):

    # -----------------------------------------------------
    # LOCALIZAÇÃO E CONTEXTO MUNICIPAL
    # -----------------------------------------------------

    st.markdown("### 1. Localização e contexto municipal")

    st.caption(
        "Selecione a unidade federativa, a rodovia, o quilômetro "
        "e informe a frota municipal."
    )

    col_uf, col_br, col_km, col_frota = st.columns(
        4,
        gap="medium",
    )

    with col_uf:
        uf = st.selectbox(
            label=FIELDS["uf"],
            options=OPTIONS["uf"],
        )

    with col_br:
        br = st.selectbox(
            label=FIELDS["br"],
            options=OPTIONS["br"],
        )

    with col_km:
        km = st.number_input(
            label=FIELDS["km"],
            min_value=0.0,
            value=0.0,
            step=1.0,
        )

    with col_frota:
        frota = st.number_input(
            label=FIELDS["frota"],
            min_value=0.0,
            value=10000.0,
            step=1000.0,
            help="Quantidade total de veículos registrados no município.",
        )

    st.divider()

    # -----------------------------------------------------
    # CARACTERÍSTICAS DA VIA
    # -----------------------------------------------------

    st.markdown("### 2. Características da via")

    st.caption(
        "Selecione as características físicas e operacionais "
        "do trecho rodoviário."
    )

    col_pista, col_uso = st.columns(
        2,
        gap="medium",
    )

    with col_pista:
        tipo_pista = st.selectbox(
            label=FIELDS["tipo_pista"],
            options=OPTIONS["tipo_pista"],
        )

    with col_uso:
        uso_solo = st.selectbox(
            label=FIELDS["uso_solo"],
            options=OPTIONS["uso_solo"],
        )

    tracado = st.multiselect(
        label="Traçado da via",
        options=TRACADOS,
        placeholder="Selecione uma ou mais características do traçado",
        help=(
            "O trecho pode apresentar mais de uma característica, "
            "como reta, curva, aclive ou interseção."
        ),
    )

    st.divider()

    # -----------------------------------------------------
    # CONTEXTO TEMPORAL E AMBIENTAL
    # -----------------------------------------------------

    st.markdown("### 3. Contexto temporal e ambiental")

    st.caption(
        "Informe quando o acidente ocorreu e quais eram "
        "as condições ambientais observadas."
    )

    col_ano, col_dia, col_fase = st.columns(
        3,
        gap="medium",
    )

    with col_ano:
        ano = st.selectbox(
            label=FIELDS["ano"],
            options=OPTIONS["ano"],
        )

    with col_dia:
        dia_semana = st.selectbox(
            label=FIELDS["dia_semana"],
            options=OPTIONS["dia_semana"],
        )

    with col_fase:
        fase_dia = st.selectbox(
            label=FIELDS["fase_dia"],
            options=OPTIONS["fase_dia"],
        )

    col_condicao, col_sentido = st.columns(
        2,
        gap="medium",
    )

    with col_condicao:
        condicao = st.selectbox(
            label=FIELDS["condicao_metereologica"],
            options=OPTIONS["condicao_metereologica"],
        )

    with col_sentido:
        sentido_via = st.selectbox(
            label=FIELDS["sentido_via"],
            options=OPTIONS["sentido_via"],
        )

    st.divider()

    # -----------------------------------------------------
    # VEÍCULO
    # -----------------------------------------------------

    st.markdown("### 4. Veículo")

    st.caption(
        "Informe o tipo de veículo ocupado pela pessoa envolvida."
    )

    tipo_veiculo = st.selectbox(
        label=FIELDS["tipo_veiculo"],
        options=OPTIONS["tipo_veiculo"],
    )

    st.markdown("")

    submitted = st.form_submit_button(
        label="Calcular probabilidade",
        width="stretch",
        type="primary",
    )


# =========================================================
# EXECUÇÃO DA PREDIÇÃO
# =========================================================

if submitted:

    dados = {
        "uf": uf,
        "br": br,
        "km": km,
        "ano": ano,
        "dia_semana": dia_semana,
        "fase_dia": fase_dia,
        "sentido_via": sentido_via,
        "condicao_metereologica": condicao,
        "tipo_pista": tipo_pista,
        "uso_solo": uso_solo,
        "tipo_veiculo": tipo_veiculo,
        "frota": frota,
        "tracado_via": tracado,
    }

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