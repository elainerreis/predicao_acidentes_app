"""
prediction_state.py

Funções responsáveis pelo gerenciamento do
estado da página de predição e atualização
dinâmica dos campos dependentes.
"""


import streamlit as st

from services.location_options import (
    km_anterior,
    primeiro_km,
    proximo_km,
)


def limpar_kms_armazenados() -> None:
    chaves = [
        chave
        for chave in st.session_state
        if chave.startswith("prediction_km_")
    ]

    for chave in chaves:
        del st.session_state[chave]


def atualizar_dependencias_uf() -> None:
    st.session_state.pop(
        "prediction_br",
        None,
    )

    limpar_kms_armazenados()


def atualizar_dependencias_br() -> None:
    limpar_kms_armazenados()


def atualizar_km_anterior(
    chave_km: str,
    intervalos: list[list[int]],
) -> None:
    valor_atual = int(
        st.session_state.get(
            chave_km,
            primeiro_km(intervalos),
        )
    )

    st.session_state[chave_km] = km_anterior(
        valor_atual,
        intervalos,
    )


def atualizar_proximo_km(
    chave_km: str,
    intervalos: list[list[int]],
) -> None:
    valor_atual = int(
        st.session_state.get(
            chave_km,
            primeiro_km(intervalos),
        )
    )

    st.session_state[chave_km] = proximo_km(
        valor_atual,
        intervalos,
    )