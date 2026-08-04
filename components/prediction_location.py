"""
prediction_location.py

Componente responsável pela seleção dinâmica
da localização do acidente (UF, BR, KM e frota),
garantindo apenas combinações válidas.
"""

import streamlit as st

from config import FIELDS
from services.location_options import (
    formatar_br,
    ordenar_brs,
    primeiro_km,
)
from services.prediction_state import (
    atualizar_dependencias_br,
    atualizar_dependencias_uf,
    atualizar_km_anterior,
    atualizar_proximo_km,
)


def show_location_fields(
    location_intervals: dict,
) -> dict:
    st.markdown(
        "### 1. Localização e contexto municipal"
    )

    st.caption(
        "Selecione a unidade federativa, a rodovia, o quilômetro "
        "e informe a frota municipal."
    )

    col_uf, col_br, col_km, col_frota = st.columns(
        4,
        gap="medium",
    )

    ufs = sorted(
        location_intervals.keys()
    )

    with col_uf:
        uf = st.selectbox(
            label=FIELDS["uf"],
            options=ufs,
            key="prediction_uf",
            on_change=atualizar_dependencias_uf,
        )

    brs = ordenar_brs(
        list(
            location_intervals
            .get(uf, {})
            .keys()
        )
    )

    if not brs:
        st.error(
            f"Nenhuma BR foi encontrada para a UF {uf}."
        )
        st.stop()

    br_atual = st.session_state.get(
        "prediction_br"
    )

    if br_atual not in brs:
        st.session_state["prediction_br"] = brs[0]

    with col_br:
        br = st.selectbox(
            label=FIELDS["br"],
            options=brs,
            format_func=formatar_br,
            key="prediction_br",
            on_change=atualizar_dependencias_br,
        )

    intervalos = (
        location_intervals
        .get(uf, {})
        .get(br, [])
    )

    if not intervalos:
        st.error(
            "Nenhum intervalo de KM foi encontrado."
        )
        st.stop()

    chave_km = f"prediction_km_{uf}_{br}"

    if chave_km not in st.session_state:
        st.session_state[chave_km] = primeiro_km(
            intervalos
        )

    with col_km:
        col_anterior, col_valor, col_proximo = st.columns(
            [1, 2.4, 1],
            gap="small",
            vertical_alignment="bottom",
        )

        with col_anterior:
            st.button(
                "−",
                key=f"previous_{uf}_{br}",
                width="stretch",
                on_click=atualizar_km_anterior,
                args=(
                    chave_km,
                    intervalos,
                ),
            )

        km = int(
            st.session_state[chave_km]
        )

        with col_valor:
            st.text_input(
                label=FIELDS["km"],
                value=str(km),
                disabled=True,
                key=(
                    f"prediction_km_display_"
                    f"{uf}_{br}_{km}"
                ),
                help=(
                    "Apenas quilômetros existentes na base de dados "
                    "para a UF e BR selecionadas podem ser utilizados."
                ),
            )

        with col_proximo:
            st.button(
                "+",
                key=f"next_{uf}_{br}",
                width="stretch",
                on_click=atualizar_proximo_km,
                args=(
                    chave_km,
                    intervalos,
                ),
            )

    with col_frota:
        frota = st.number_input(
            label=FIELDS["frota"],
            min_value=0.0,
            value=10000.0,
            step=1000.0,
            key="prediction_frota",
        )

    return {
        "uf": uf,
        "br": br,
        "km": float(km),
        "frota": frota,
    }