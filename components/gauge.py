import plotly.graph_objects as go
import streamlit as st


def show_gauge(probabilidade: float):
    """
    Exibe um velocímetro representando a probabilidade
    de ocorrência de acidente grave.

    Parameters
    ----------
    probabilidade : float
        Valor entre 0 e 1.
    """

    valor = probabilidade * 100

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=valor,
            number={
                "suffix": "%",
                "font": {"size": 42}
            },
            title={
                "text": "Probabilidade de acidente grave",
                "font": {"size": 20}
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1
                },
                "bar": {
                    "thickness": 0.35
                },
                "steps": [
                    {
                        "range": [0, 30],
                        "color": "#4CAF50"
                    },
                    {
                        "range": [30, 70],
                        "color": "#FFC107"
                    },
                    {
                        "range": [70, 100],
                        "color": "#F44336"
                    },
                ],
                "threshold": {
                    "line": {
                        "color": "black",
                        "width": 5
                    },
                    "value": valor
                },
            },
        )
    )

    fig.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )