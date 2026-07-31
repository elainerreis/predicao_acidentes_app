"""
home_model_global_shap.py

Gráficos SHAP globais utilizando Plotly.
"""

import copy
from typing import Any

import numpy as np
import pandas as pd
import plotly.express as px
import shap
import streamlit as st


# =====================================================
# CONFIGURAÇÕES
# =====================================================

COLOR = "#1565C0"


TRACADOS = [
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
]


NOMES_VARIAVEIS = {
    "uf": "Estado (UF)",
    "br": "Rodovia (BR)",
    "br_km": "Trecho (BR + KM)",
    "dia_semana": "Dia da Semana",
    "fase_dia": "Fase do Dia",
    "sentido_via": "Sentido da Via",
    "condicao_metereologica": "Condição Meteorológica",
    "condicao_meteorologica": "Condição Meteorológica",
    "tipo_pista": "Tipo de Pista",
    "uso_solo": "Perímetro",
    "tipo_veiculo": "Tipo de Veículo",
    "ano": "Ano",
    "frota": "Frota",
    "tracado_via": "Traçado da Via",
}


# =====================================================
# FORMATAÇÃO
# =====================================================

def _formatar_impacto(
    valor: Any,
) -> str:
    """
    Formata um valor SHAP com duas casas decimais
    e vírgula como separador decimal.

    Exemplos:
        0.4567 -> 0,46
        1.0    -> 1,00
    """

    try:
        numero = float(valor)

        return (
            f"{numero:.2f}"
            .replace(".", ",")
        )

    except (TypeError, ValueError):
        return str(valor)


# =====================================================
# AGRUPA O TRAÇADO DA VIA
# =====================================================

def agrupar_tracado(
    shap_values,
):
    """
    Agrupa as colunas binárias de traçado da via
    em uma única variável global.
    """

    shap_values = copy.deepcopy(
        shap_values
    )

    valores = np.asarray(
        shap_values.values
    ).copy()

    dados = (
        np.asarray(
            shap_values.data
        ).copy()
        if shap_values.data is not None
        else None
    )

    nomes = list(
        shap_values.feature_names
    )

    indices = []

    for indice, nome in enumerate(nomes):
        nome = str(nome)

        if (
            nome in TRACADOS
            or any(
                nome.startswith(tracado)
                for tracado in TRACADOS
            )
        ):
            indices.append(indice)

    if len(indices) <= 1:
        return shap_values

    indice_mestre = indices[0]
    indices_remover = indices[1:]

    valores[:, indice_mestre] = valores[
        :,
        indices,
    ].sum(
        axis=1
    )

    if dados is not None:
        dados[:, indice_mestre] = dados[
            :,
            indices,
        ].sum(
            axis=1
        )

    nomes[indice_mestre] = "tracado_via"

    valores = np.delete(
        valores,
        indices_remover,
        axis=1,
    )

    if dados is not None:
        dados = np.delete(
            dados,
            indices_remover,
            axis=1,
        )

    nomes = [
        nome
        for indice, nome in enumerate(nomes)
        if indice not in indices_remover
    ]

    return shap.Explanation(
        values=valores,
        data=dados,
        feature_names=nomes,
        base_values=shap_values.base_values,
    )


# =====================================================
# RENOMEIA AS FEATURES
# =====================================================

def renomear_features(
    shap_values,
):
    """
    Substitui os nomes técnicos das variáveis
    por nomes mais claros para apresentação.
    """

    shap_values = copy.deepcopy(
        shap_values
    )

    novos_nomes = []

    for nome in shap_values.feature_names:
        nome = str(nome)

        novos_nomes.append(
            NOMES_VARIAVEIS.get(
                nome,
                nome,
            )
        )

    shap_values.feature_names = novos_nomes

    return shap_values

# =====================================================
# ANÁLISE TEXTUAL DO SHAP GLOBAL
# =====================================================

def show_global_shap_analysis(
    shap_values,
    quantidade_variaveis: int = 5,
):
    """
    Exibe uma análise textual automática das variáveis
    com maior importância global segundo os valores SHAP.

    A importância é calculada pela média do valor absoluto
    dos valores SHAP.
    """

    if shap_values is None:
        st.warning(
            "Os valores SHAP não estão disponíveis "
            "para gerar a análise."
        )
        return

    try:
        # Agrupa as variáveis binárias de traçado.
        shap_plot = agrupar_tracado(
            shap_values
        )

        # Substitui nomes técnicos por nomes amigáveis.
        shap_plot = renomear_features(
            shap_plot
        )

        valores_shap = np.asarray(
            shap_plot.values
        )

        impactos = np.abs(
            valores_shap
        ).mean(
            axis=0
        )

        df = pd.DataFrame(
            {
                "Variável": shap_plot.feature_names,
                "Impacto": impactos,
            }
        )

        df = (
            df.sort_values(
                by="Impacto",
                ascending=False,
            )
            .reset_index(drop=True)
        )

        quantidade = min(
            quantidade_variaveis,
            len(df),
        )

        principais = df.head(
            quantidade
        )

        primeira = principais.iloc[0]
        segunda = (
            principais.iloc[1]
            if len(principais) > 1
            else None
        )

        nomes_principais = principais[
            "Variável"
        ].tolist()

        if len(nomes_principais) == 1:
            lista_variaveis = nomes_principais[0]

        elif len(nomes_principais) == 2:
            lista_variaveis = (
                f"{nomes_principais[0]} e "
                f"{nomes_principais[1]}"
            )

        else:
            lista_variaveis = (
                ", ".join(
                    nomes_principais[:-1]
                )
                + f" e {nomes_principais[-1]}"
            )

        impacto_primeira = _formatar_impacto(
            primeira["Impacto"]
        )

        texto_segunda = ""

        if segunda is not None:
            impacto_segunda = _formatar_impacto(
                segunda["Impacto"]
            )

            texto_segunda = (
                f" Em seguida aparece "
                f"**{segunda['Variável']}**, com impacto "
                f"médio absoluto de **{impacto_segunda}**."
            )

        st.markdown(
            f"""
### Análise da importância global

A variável com maior influência nas previsões do modelo foi
**{primeira['Variável']}**, com impacto médio absoluto de
**{impacto_primeira}**.{texto_segunda}

De forma geral, as variáveis que mais contribuíram para as
decisões do modelo foram **{lista_variaveis}**. 

É importante observar que este gráfico apresenta a
**magnitude média da influência** de cada variável. Portanto,
uma variável mais importante participa mais intensamente das
previsões, mas o gráfico não informa, isoladamente, se ela
aumenta ou reduz a probabilidade de gravidade.

Os resultados devem ser interpretados como associações
aprendidas pelo modelo a partir dos registros históricos, e
não como relações diretas de causa e efeito.
"""
        )

    except Exception as erro:
        st.error(
            "Não foi possível gerar a análise textual "
            f"do SHAP global: {erro}"
        )

# =====================================================
# SHAP GLOBAL
# =====================================================

def show_global_shap(
    shap_values,
):
    """
    Exibe a importância global das variáveis,
    calculada pela média do valor absoluto do SHAP.
    """

    if shap_values is None:
        st.warning(
            "Os valores SHAP não estão disponíveis."
        )
        return

    try:
        # Agrupa as dummies de traçado em uma variável.
        shap_plot = agrupar_tracado(
            shap_values
        )

        # Renomeia as variáveis.
        shap_plot = renomear_features(
            shap_plot
        )

        valores_shap = np.asarray(
            shap_plot.values
        )

        # Calcula a importância global usando os valores
        # completos, antes de realizar o arredondamento.
        impactos = np.abs(
            valores_shap
        ).mean(
            axis=0
        )

        df = pd.DataFrame(
            {
                "Variável": shap_plot.feature_names,
                "Impacto original": impactos,
            }
        )

        # Valor numérico usado para desenhar as barras.
        df["Impacto"] = (
            pd.to_numeric(
                df["Impacto original"],
                errors="coerce",
            )
            .round(2)
        )

        df = df.dropna(
            subset=["Impacto"]
        )

        # Valor textual mostrado sobre as barras
        # e no tooltip.
        df["Impacto formatado"] = (
            df["Impacto"]
            .apply(_formatar_impacto)
        )

        df = df.sort_values(
            by="Impacto",
            ascending=True,
        )

        if df.empty:
            st.warning(
                "Não há valores SHAP globais "
                "disponíveis para exibição."
            )
            return

        altura = max(
            550,
            len(df) * 35,
        )

        fig = px.bar(
            df,
            x="Impacto",
            y="Variável",
            orientation="h",
            text="Impacto formatado",
            custom_data=[
                "Impacto formatado",
            ],
        )

        fig.update_traces(
            marker_color=COLOR,
            texttemplate="%{text}",
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Impacto médio absoluto (|SHAP|): "
                "%{customdata[0]}"
                "<extra></extra>"
            ),
        )

        fig.update_layout(
            title="Importância Global das Variáveis (SHAP)",
            xaxis_title=(
                "Impacto médio absoluto (|SHAP|)"
            ),
            yaxis_title="",
            showlegend=False,
            height=altura,
            separators=",.",
            margin=dict(
                l=10,
                r=80,
                t=50,
                b=10,
            ),
            bargap=0.25,
        )

        fig.update_xaxes(
            tickformat=".2f",
            zeroline=False,
            gridcolor="rgba(0, 0, 0, 0.10)",
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
            "Não foi possível gerar o gráfico "
            f"SHAP global: {erro}"
        )


# =====================================================
# TRAÇADO DA VIA
# =====================================================

def show_tracado_shap(
    shap_values,
):
    """
    Exibe o impacto global individual dos diferentes
    tipos de traçado da via.
    """

    st.subheader(
        "Impacto dos Diferentes Traçados da Via"
    )

    if shap_values is None:
        st.warning(
            "Os valores SHAP não estão disponíveis."
        )
        return

    try:
        nomes = list(
            shap_values.feature_names
        )

        valores_shap = np.asarray(
            shap_values.values
        )

        importancia = []

        for tracado in TRACADOS:
            indice_encontrado = None

            for indice, nome in enumerate(nomes):
                nome = str(nome)

                if (
                    nome == tracado
                    or nome.startswith(tracado)
                ):
                    indice_encontrado = indice
                    break

            if indice_encontrado is None:
                continue

            impacto = np.abs(
                valores_shap[
                    :,
                    indice_encontrado,
                ]
            ).mean()

            importancia.append(
                {
                    "Traçado": tracado,
                    "Impacto original": impacto,
                }
            )

        if not importancia:
            st.warning(
                "Nenhuma variável de traçado "
                "foi encontrada."
            )
            return

        df = pd.DataFrame(
            importancia
        )

        # Valor numérico arredondado usado no gráfico.
        df["Impacto"] = (
            pd.to_numeric(
                df["Impacto original"],
                errors="coerce",
            )
            .round(2)
        )

        df = df.dropna(
            subset=["Impacto"]
        )

        # Valor textual no padrão brasileiro.
        df["Impacto formatado"] = (
            df["Impacto"]
            .apply(_formatar_impacto)
        )

        df = df.sort_values(
            by="Impacto",
            ascending=True,
        )

        if df.empty:
            st.warning(
                "Não há valores SHAP de traçado "
                "disponíveis para exibição."
            )
            return

        altura = max(
            520,
            len(df) * 38,
        )

        fig = px.bar(
            df,
            x="Impacto",
            y="Traçado",
            orientation="h",
            text="Impacto formatado",
            custom_data=[
                "Impacto formatado",
            ],
        )

        fig.update_traces(
            marker_color=COLOR,
            texttemplate="%{text}",
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Impacto médio absoluto (|SHAP|): "
                "%{customdata[0]}"
                "<extra></extra>"
            ),
        )

        fig.update_layout(
            title=(
                "Impacto dos Diferentes "
                "Traçados da Via"
            ),
            height=altura,
            showlegend=False,
            xaxis_title=(
                "Impacto médio absoluto (|SHAP|)"
            ),
            yaxis_title="",
            separators=",.",
            margin=dict(
                l=10,
                r=80,
                t=45,
                b=10,
            ),
            bargap=0.25,
        )

        fig.update_xaxes(
            tickformat=".2f",
            zeroline=False,
            gridcolor="rgba(0, 0, 0, 0.10)",
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
            "Não foi possível gerar o gráfico "
            f"SHAP dos traçados: {erro}"
        )