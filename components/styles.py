"""
styles.py

Carrega e aplica os estilos CSS globais da aplicação.
"""

from pathlib import Path

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parent.parent
CSS_PATH = ROOT_DIR / "assets" / "css" / "style.css"


def apply_styles() -> None:
    """
    Carrega o arquivo CSS global e aplica os estilos
    à aplicação Streamlit.
    """

    if not CSS_PATH.exists():
        st.warning(
            f"Arquivo de estilos não encontrado: {CSS_PATH}"
        )
        return

    css = CSS_PATH.read_text(
        encoding="utf-8"
    )

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )