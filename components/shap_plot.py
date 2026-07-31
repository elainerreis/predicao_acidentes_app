"""
shap_plot.py

Gráfico local dos valores SHAP utilizando Plotly.
"""

from typing import Any

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# CONFIGURAÇÕES VISUAIS
# =========================================================

COR_POSITIVA = "#E53935"
COR_NEGATIVA = "#1565C0"


# =========================================================
# NOMES AMIGÁVEIS
# =========================================================

FEATURE_NAMES = {
    "uf": "Estado (UF)",
    "br": "Rodovia (BR)",
    "dia_semana": "Dia da semana",
    "fase_dia": "Fase do dia",
    "sentido_via": "Sentido da via",
    "condicao_metereologica": "Condição meteorológica",
    "tipo_pista": "Tipo de pista",
    "uso_solo": "Perímetro Urbano",
    "tipo_veiculo": "Tipo de veículo",
    "ano": "Ano",
    "frota": "Frota municipal",
    "br_km": "Trecho da rodovia",
}


TRACADOS = {
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
}


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def _obter_vetor(
    valor: Any,
) -> np.ndarray:
    """
    Converte os valores recebidos em vetor unidimensional.
    """

    vetor = np.asarray(valor)

    if vetor.ndim == 0:
        return vetor.reshape(1)

    if vetor.ndim == 1:
        return vetor

    if vetor.ndim == 2:
        return vetor[0]

    return vetor.reshape(-1)


def _tracado_selecionado(
    valor: Any,
) -> bool:
    """
    Verifica se uma dummy de traçado está ativa.
    """

    try:
        return int(float(valor)) == 1

    except (TypeError, ValueError):
        return False


def _formatar_br(
    valor: Any,
) -> str:
    """
    Formata a rodovia no padrão BR-XXX.
    """

    if valor is None:
        return "BR não informada"

    texto = str(valor).strip().upper()

    if not texto:
        return "BR não informada"

    if texto.startswith("BR-"):
        return texto

    if texto.startswith("BR"):
        numero = texto[2:].strip("- ")
        return f"BR-{numero}"

    try:
        numero = int(float(texto))
        return f"BR-{numero}"

    except (TypeError, ValueError):
        return f"BR-{texto}"


def _formatar_km(
    valor: Any,
) -> str:
    """
    Formata o quilômetro para apresentação.
    """

    if valor is None:
        return "não informado"

    try:
        numero = float(valor)

        if numero.is_integer():
            return str(int(numero))

        return (
            f"{numero:.1f}"
            .replace(".", ",")
        )

    except (TypeError, ValueError):
        return str(valor)


def _formatar_valor(
    feature: str,
    valor: Any,
) -> str:
    """
    Formata os valores das variáveis para exibição.
    """

    if valor is None:
        return "não informado"

    if feature == "br":
        return _formatar_br(valor)

    if feature == "ano":
        try:
            return str(
                int(float(valor))
            )

        except (TypeError, ValueError):
            return str(valor)

    if feature == "frota":
        try:
            return (
                f"{float(valor):,.0f}"
                .replace(",", ".")
            )

        except (TypeError, ValueError):
            return str(valor)

    if isinstance(
        valor,
        (float, np.floating),
    ):
        if np.isnan(valor):
            return "não informado"

        if float(valor).is_integer():
            return str(int(valor))

        return (
            f"{valor:.2f}"
            .replace(".", ",")
        )

    return str(valor)


def _formatar_impacto(
    valor: float,
) -> str:
    """
    Formata o valor SHAP com sinal,
    duas casas decimais e vírgula.
    """

    return (
        f"{valor:+.2f}"
        .replace(".", ",")
    )


def _criar_label(
    feature: str,
    valor: Any,
    dados_entrada: dict,
) -> str:
    """
    Cria o rótulo amigável mostrado no gráfico.
    """

    if feature in TRACADOS:
        return (
            f"Traçado da via: {feature}"
        )

    if feature == "br_km":
        br = _formatar_br(
            dados_entrada.get("br")
        )

        km = _formatar_km(
            dados_entrada.get("km")
        )

        return (
            f"Trecho da rodovia: "
            f"{br}, km {km}"
        )

    if feature == "br":
        br = _formatar_br(
            dados_entrada.get(
                "br",
                valor,
            )
        )

        return f"Rodovia (BR): {br}"

    nome = FEATURE_NAMES.get(
        feature,
        feature
        .replace("_", " ")
        .strip()
        .capitalize(),
    )

    valor_formatado = _formatar_valor(
        feature,
        valor,
    )

    return (
        f"{nome}: {valor_formatado}"
    )


# =========================================================
# GRÁFICO SHAP LOCAL
# =========================================================

def show_shap_plot(
    explanation: Any,
    dados_entrada: dict | None = None,
) -> None:
    """
    Exibe um gráfico horizontal dos valores SHAP.

    São mostradas todas as variáveis comuns e somente
    as opções de traçado selecionadas no formulário.
    """

    if explanation is None:
        st.warning(
            "A explicação SHAP não está disponível "
            "para esta previsão."
        )
        return

    dados_entrada = dados_entrada or {}

    try:
        values = _obter_vetor(
            explanation.values
        )

        names = list(
            explanation.feature_names
        )

        data = _obter_vetor(
            explanation.data
        )

        quantidade = min(
            len(values),
            len(names),
            len(data),
        )

        df = pd.DataFrame(
            {
                "feature": names[:quantidade],
                "valor": data[:quantidade],
                "shap": values[:quantidade],
            }
        )

        df["shap"] = pd.to_numeric(
            df["shap"],
            errors="coerce",
        )

        df = df.dropna(
            subset=["shap"]
        )

        # Remove somente os traçados não selecionados.
        mascara_tracado_nao_selecionado = (
            df["feature"].isin(TRACADOS)
            & ~df["valor"].apply(
                _tracado_selecionado
            )
        )

        df = df[
            ~mascara_tracado_nao_selecionado
        ].copy()

        if df.empty:
            st.warning(
                "Não há contribuições SHAP "
                "disponíveis para exibição."
            )
            return

        df["Variável"] = df.apply(
            lambda row: _criar_label(
                feature=str(
                    row["feature"]
                ),
                valor=row["valor"],
                dados_entrada=dados_entrada,
            ),
            axis=1,
        )

        # Arredonda efetivamente os valores usados no gráfico.
        df["Impacto"] = df["shap"].round(2)

        # Cria o texto já formatado no padrão brasileiro.
        df["Impacto formatado"] = df["Impacto"].apply(
            _formatar_impacto
        )

        df["Direção"] = np.where(
            df["Impacto"] >= 0,
            "Aumenta a estimativa",
            "Reduz a estimativa",
        )

        # Ordena do impacto mais negativo
        # para o mais positivo.
        df = df.sort_values(
            by="Impacto",
            ascending=True,
        )

        altura = max(
            550,
            len(df) * 38,
        )

        fig = px.bar(
            df,
            x="Impacto",
            y="Variável",
            orientation="h",

            # Usa o texto já formatado,
            # evitando depender do locale do Plotly.
            text="Impacto formatado",

            color="Direção",
            color_discrete_map={
                "Aumenta a estimativa": COR_POSITIVA,
                "Reduz a estimativa": COR_NEGATIVA,
            },

            custom_data=[
                "Impacto formatado",
                "Direção",
            ],
        )

        fig.update_traces(
            texttemplate="%{text}",
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Valor SHAP: %{customdata[0]}<br>"
                "Efeito: %{customdata[1]}"
                "<extra></extra>"
            ),
        )

        fig.add_vline(
            x=0,
            line_width=1,
            line_color="#333333",
        )

        fig.update_layout(
            title=(
                "Fatores que influenciaram "
                "a previsão"
            ),
            xaxis_title=(
                "Impacto na predição "
                "(valor SHAP)"
            ),
            yaxis_title="",
            height=altura,
            showlegend=True,
            legend_title_text="",

            # Vírgula decimal e ponto para milhares.
            separators=",.",

            margin=dict(
                l=10,
                r=90,
                t=60,
                b=20,
            ),
            bargap=0.25,
        )

        fig.update_xaxes(
            zeroline=False,
            gridcolor="rgba(0, 0, 0, 0.10)",
            tickformat=".2f",
        )

        fig.update_yaxes(
            automargin=True,
        )

        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displaylogo": False,
                "responsive": True,
            },
        )

    except Exception as erro:
        st.error(
            "Não foi possível gerar o gráfico SHAP: "
            f"{erro}"
        )