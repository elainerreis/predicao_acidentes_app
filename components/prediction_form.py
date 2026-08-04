"""
prediction_form.py

Componente responsável pela construção da
interface da página de predição e coleta
dos dados informados pelo usuário.
"""

from typing import Any

import streamlit as st

from config import FIELDS, OPTIONS, TRACADOS
from components.prediction_location import (
    show_location_fields,
)
from services.location_options import (
    obter_ordem_exibicao,
    ordenar_opcoes,
)


def show_prediction_form(
    metadata: dict[str, Any],
) -> dict | None:
    location_intervals = metadata.get(
        "location_intervals",
        {},
    )

    if not location_intervals:
        st.error(
            "O metadata não contém os intervalos de localização."
        )
        return None

    ordem_dias = obter_ordem_exibicao(
        metadata,
        "dia_semana",
        [
            "segunda-feira",
            "terça-feira",
            "quarta-feira",
            "quinta-feira",
            "sexta-feira",
            "sábado",
            "domingo",
        ],
    )

    ordem_fases = obter_ordem_exibicao(
        metadata,
        "fase_dia",
        [
            "Plena Noite",
            "Amanhecer",
            "Pleno dia",
            "Anoitecer",
        ],
    )

    dias = ordenar_opcoes(
        OPTIONS["dia_semana"],
        ordem_dias,
    )

    fases = ordenar_opcoes(
        OPTIONS["fase_dia"],
        ordem_fases,
    )

    with st.container(
        key="prediction_form",
    ):
        localizacao = show_location_fields(
            location_intervals
        )

        st.divider()
        st.markdown("### 2. Características da via")

        col_pista, col_uso = st.columns(2)

        with col_pista:
            tipo_pista = st.selectbox(
                FIELDS["tipo_pista"],
                OPTIONS["tipo_pista"],
            )

        with col_uso:
            uso_solo = st.selectbox(
                FIELDS["uso_solo"],
                OPTIONS["uso_solo"],
            )

        tracado = st.multiselect(
            "Traçado da via",
            TRACADOS,
        )

        st.divider()
        st.markdown(
            "### 3. Contexto temporal e ambiental"
        )

        col_ano, col_dia, col_fase = st.columns(3)

        with col_ano:
            ano = st.selectbox(
                FIELDS["ano"],
                OPTIONS["ano"],
            )

        with col_dia:
            dia_semana = st.selectbox(
                FIELDS["dia_semana"],
                dias,
            )

        with col_fase:
            fase_dia = st.selectbox(
                FIELDS["fase_dia"],
                fases,
            )

        col_condicao, col_sentido = st.columns(2)

        with col_condicao:
            condicao = st.selectbox(
                FIELDS["condicao_metereologica"],
                OPTIONS["condicao_metereologica"],
            )

        with col_sentido:
            sentido = st.selectbox(
                FIELDS["sentido_via"],
                OPTIONS["sentido_via"],
            )

        st.divider()
        st.markdown("### 4. Veículo")

        tipo_veiculo = st.selectbox(
            FIELDS["tipo_veiculo"],
            OPTIONS["tipo_veiculo"],
        )

        submitted = st.button(
            "Calcular probabilidade",
            width="stretch",
            type="primary",
        )

    if not submitted:
        return None

    return {
        **localizacao,
        "ano": ano,
        "dia_semana": dia_semana,
        "fase_dia": fase_dia,
        "sentido_via": sentido,
        "condicao_metereologica": condicao,
        "tipo_pista": tipo_pista,
        "uso_solo": uso_solo,
        "tipo_veiculo": tipo_veiculo,
        "tracado_via": tracado,
    }