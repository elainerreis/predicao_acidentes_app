"""
predict_analysis.py

Responsável por apresentar e interpretar o resultado
da predição realizada pelo modelo.
"""

from typing import Any

import numpy as np
import streamlit as st

from components.gauge import show_gauge
from components.shap_plot import show_shap_plot


# =========================================================
# NOMES AMIGÁVEIS DAS VARIÁVEIS
# =========================================================

FEATURE_LABELS = {
    "uf": "Unidade federativa",
    "br": "Rodovia",
    "br_km": "Trecho da rodovia",
    "dia_semana": "Dia da semana",
    "fase_dia": "Fase do dia",
    "sentido_via": "Sentido da via",
    "condicao_metereologica": "Condição meteorológica",
    "tipo_pista": "Tipo de pista",
    "uso_solo": "Perímetro Urbano",
    "tipo_veiculo": "Tipo de veículo",
    "ano": "Ano",
    "frota": "Frota municipal",
    "Aclive": "Aclive",
    "Curva": "Curva",
    "Declive": "Declive",
    "Desvio Temporário": "Desvio temporário",
    "Em Obras": "Trecho em obras",
    "Interseção de Vias": "Interseção de vias",
    "Ponte": "Ponte",
    "Reta": "Reta",
    "Retorno Regulamentado": "Retorno regulamentado",
    "Rotatória": "Rotatória",
    "Túnel": "Túnel",
    "Viaduto": "Viaduto",
}


# Variáveis binárias geradas a partir de tracado_via.
TRACADOS_BINARIOS = {
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
# INTERPRETAÇÃO DA PROBABILIDADE
# =========================================================

def interpretar_probabilidade(
    probabilidade: float,
) -> dict:
    """
    Classifica a probabilidade estimada e produz
    uma interpretação textual.
    """

    percentual = probabilidade * 100

    if probabilidade < 0.30:
        return {
            "nivel": "Baixa",
            "tipo": "success",
            "texto": (
                f"O modelo estimou uma probabilidade de "
                f"**{percentual:.2f}%** de o cenário resultar em "
                "lesões graves ou óbito. O valor está situado na "
                "faixa de baixa probabilidade definida para a aplicação."
            ),
        }

    if probabilidade < 0.70:
        return {
            "nivel": "Moderada",
            "tipo": "warning",
            "texto": (
                f"O modelo estimou uma probabilidade de "
                f"**{percentual:.2f}%** de o cenário resultar em "
                "lesões graves ou óbito. O resultado está situado "
                "na faixa intermediária e indica a presença de "
                "características que merecem atenção."
            ),
        }

    return {
        "nivel": "Alta",
        "tipo": "error",
        "texto": (
            f"O modelo estimou uma probabilidade de "
            f"**{percentual:.2f}%** de o cenário resultar em "
            "lesões graves ou óbito. O resultado está situado na "
            "faixa de alta probabilidade, indicando que as "
            "características informadas apresentam forte associação "
            "com casos graves nos dados históricos analisados."
        ),
    }


# =========================================================
# FUNÇÕES DE FORMATAÇÃO
# =========================================================

def _formatar_nome_variavel(
    nome: str,
) -> str:
    """
    Converte o nome técnico da variável em um nome amigável.
    """

    if nome in FEATURE_LABELS:
        return FEATURE_LABELS[nome]

    return (
        nome
        .replace("_", " ")
        .strip()
        .capitalize()
    )


def _formatar_br(
    valor: Any,
) -> str:
    """
    Formata a rodovia no padrão BR-XXX.
    """

    if valor is None:
        return "BR não informada"

    texto = str(valor).strip()

    if not texto:
        return "BR não informada"

    texto = texto.upper()

    if texto.startswith("BR-"):
        return texto

    if texto.startswith("BR"):
        numero = texto[2:].strip("- ")
        return f"BR-{numero}"

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
    nome: str,
    valor: Any,
) -> str:
    """
    Formata o valor de uma variável de acordo
    com seu tipo e significado.
    """

    if valor is None:
        return "não informado"

    # Variáveis de traçado são binárias.
    if nome in TRACADOS_BINARIOS:
        try:
            return (
                "Presente"
                if int(float(valor)) == 1
                else "Ausente"
            )
        except (TypeError, ValueError):
            return str(valor)

    if isinstance(valor, (bool, np.bool_)):
        return "Sim" if valor else "Não"

    if isinstance(valor, (int, np.integer)):
        return f"{int(valor):,}".replace(",", ".")

    if isinstance(valor, (float, np.floating)):
        if np.isnan(valor):
            return "não informado"

        if nome == "frota":
            return (
                f"{valor:,.0f}"
                .replace(",", ".")
            )

        if float(valor).is_integer():
            return str(int(valor))

        return (
            f"{valor:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    return str(valor)


def _formatar_fator_shap(
    nome: str,
    valor: Any,
    dados_entrada: dict,
) -> str:
    """
    Formata uma variável e seu valor para o texto SHAP.

    As dummies de traçado são apresentadas como uma única
    variável conceitual: Traçado da via.
    """

    # As dummies de traçado representam categorias
    # da variável original tracado_via.
    if nome in TRACADOS_BINARIOS:
        return f"**Traçado da via** ({nome})"

    nome_amigavel = _formatar_nome_variavel(nome)

    if nome == "br_km":
        br = _formatar_br(
            dados_entrada.get("br")
        )

        km = _formatar_km(
            dados_entrada.get("km")
        )

        return (
            f"**{nome_amigavel}** "
            f"({br}, km {km})"
        )

    if nome == "br":
        br = _formatar_br(
            dados_entrada.get(
                "br",
                valor,
            )
        )

        return (
            f"**{nome_amigavel}** "
            f"({br})"
        )

    valor_formatado = _formatar_valor(
        nome,
        valor,
    )

    return (
        f"**{nome_amigavel}** "
        f"({valor_formatado})"
    )


# =========================================================
# EXTRAÇÃO DOS VALORES SHAP
# =========================================================

def _obter_vetor(
    valor: Any,
) -> np.ndarray:
    """
    Converte uma estrutura SHAP em vetor unidimensional.
    """

    vetor = np.asarray(valor)

    if vetor.ndim == 0:
        return vetor.reshape(1)

    if vetor.ndim == 1:
        return vetor

    if vetor.ndim == 2:
        return vetor[0]

    return vetor.reshape(-1)

def _tracado_selecionado(valor: Any) -> bool:
    """
    Verifica se uma dummy de traçado está ativa.
    """

    try:
        return int(float(valor)) == 1

    except (TypeError, ValueError):
        return False
    
def interpretar_shap(
    explanation: Any,
    dados_entrada: dict,
    top_n: int = 3,
) -> dict:
    """
    Identifica as principais variáveis que aumentaram
    ou reduziram a estimativa de gravidade.
    """

    if explanation is None:
        return {
            "disponivel": False,
            "texto": (
                "A interpretação dos fatores associados à previsão "
                "não está disponível para este cenário."
            ),
            "aumentam": [],
            "reduzem": [],
        }

    try:
        shap_values = _obter_vetor(
            explanation.values
        )

        feature_values = _obter_vetor(
            explanation.data
        )

        feature_names = list(
            explanation.feature_names
        )

    except (AttributeError, TypeError, ValueError):
        return {
            "disponivel": False,
            "texto": (
                "Não foi possível extrair automaticamente as "
                "contribuições SHAP desta previsão."
            ),
            "aumentam": [],
            "reduzem": [],
        }

    quantidade = min(
        len(shap_values),
        len(feature_values),
        len(feature_names),
    )

    contribuicoes = []

    for indice in range(quantidade):
        nome = str(
            feature_names[indice]
        )

        valor = feature_values[indice]

        valor_shap = float(
            shap_values[indice]
        )

        if not np.isfinite(valor_shap):
            continue

        # Entre as dummies de traçado, considera somente
        # as opções selecionadas no formulário.
        if (
            nome in TRACADOS_BINARIOS
            and not _tracado_selecionado(valor)
        ):
            continue

        contribuicoes.append(
            {
                "variavel": nome,
                "valor": valor,
                "shap": valor_shap,
            }
        )
    aumentam = sorted(
        [
            item
            for item in contribuicoes
            if item["shap"] > 0
        ],
        key=lambda item: item["shap"],
        reverse=True,
    )[:top_n]

    reduzem = sorted(
        [
            item
            for item in contribuicoes
            if item["shap"] < 0
        ],
        key=lambda item: item["shap"],
    )[:top_n]

    partes = []

    if aumentam:
        fatores_positivos = ", ".join(
            _formatar_fator_shap(
                nome=item["variavel"],
                valor=item["valor"],
                dados_entrada=dados_entrada,
            )
            for item in aumentam
        )

        partes.append(
            "Os fatores que mais contribuíram para "
            "aumentar a estimativa de gravidade foram: "
            f"{fatores_positivos}."
        )

    if reduzem:
        fatores_negativos = ", ".join(
            _formatar_fator_shap(
                nome=item["variavel"],
                valor=item["valor"],
                dados_entrada=dados_entrada,
            )
            for item in reduzem
        )

        partes.append(
            "Em sentido contrário, os fatores que mais "
            "contribuíram para reduzir a estimativa foram: "
            f"{fatores_negativos}."
        )

    if partes:
        texto = " ".join(partes)
    else:
        texto = (
            "Não foram identificadas contribuições SHAP "
            "individuais relevantes para esta previsão."
        )

    texto += (
        " Essas contribuições representam o comportamento do "
        "modelo neste cenário específico e não estabelecem "
        "uma relação de causa e efeito."
    )

    return {
        "disponivel": True,
        "texto": texto,
        "aumentam": aumentam,
        "reduzem": reduzem,
    }


# =========================================================
# MENSAGEM DA PROBABILIDADE
# =========================================================

def _exibir_mensagem_probabilidade(
    interpretacao: dict,
) -> None:
    """
    Exibe a interpretação da probabilidade na caixa adequada.
    """

    tipo = interpretacao["tipo"]
    texto = interpretacao["texto"]

    if tipo == "success":
        st.success(texto)

    elif tipo == "warning":
        st.warning(texto)

    else:
        st.error(texto)


# =========================================================
# RESULTADO DA PREDIÇÃO
# =========================================================

def show_prediction(
    resultado: dict,
) -> None:
    """
    Exibe as métricas, o gauge, a interpretação
    da probabilidade e a explicação SHAP.
    """

    probabilidade = float(
        resultado["probabilidade"]
    )

    percentual = float(
        resultado["percentual"]
    )

    classe = int(
        resultado["classe"]
    )

    classificacao_modelo = resultado["risco"]

    explanation = resultado.get(
        "explanation"
    )

    dados_entrada = resultado.get(
        "dados_entrada",
        {},
    )

    interpretacao_probabilidade = interpretar_probabilidade(
        probabilidade
    )

    interpretacao_local = interpretar_shap(
        explanation=explanation,
        dados_entrada=dados_entrada,
        top_n=3,
    )

    # -----------------------------------------------------
    # CABEÇALHO DO RESULTADO
    # -----------------------------------------------------

    st.caption(
        "Estimativa produzida pelo modelo a partir das "
        "características informadas para o cenário."
    )

    # -----------------------------------------------------
    # MÉTRICAS
    # -----------------------------------------------------

    col_probabilidade, col_faixa, col_classe = st.columns(
        3,
        gap="medium",
    )

    with col_probabilidade:
        st.metric(
            label="Probabilidade estimada",
            value=f"{percentual:.2f}%",
        )

    with col_faixa:
        st.metric(
            label="Faixa de probabilidade",
            value=interpretacao_probabilidade["nivel"],
        )

    with col_classe:
        st.metric(
            label="Classificação do modelo",
            value=classificacao_modelo,
        )

    # -----------------------------------------------------
    # GAUGE
    # -----------------------------------------------------

    show_gauge(
        probabilidade
    )

    # -----------------------------------------------------
    # INTERPRETAÇÃO DA PROBABILIDADE
    # -----------------------------------------------------

    st.markdown(
        "### Interpretação do resultado"
    )

    _exibir_mensagem_probabilidade(
        interpretacao_probabilidade
    )

    # -----------------------------------------------------
    # INTERPRETAÇÃO SHAP
    # -----------------------------------------------------

    st.markdown(
        "### Fatores associados à previsão"
    )

    st.markdown(
        interpretacao_local["texto"]
    )

    # -----------------------------------------------------
    # GRÁFICO SHAP
    # -----------------------------------------------------

    st.markdown(
        "### Contribuição das variáveis"
    )

    st.caption(
        "Valores positivos aumentam a estimativa da classe "
        "grave, enquanto valores negativos reduzem essa estimativa."
    )

    show_shap_plot(
        explanation=explanation,
        dados_entrada=dados_entrada,
    )

    # -----------------------------------------------------
    # DETALHES TÉCNICOS
    # -----------------------------------------------------

    with st.expander(
        "Detalhes técnicos da predição"
    ):
        st.json(
            {
                "classe_predita": classe,
                "classificacao_modelo": classificacao_modelo,
                "probabilidade": probabilidade,
                "percentual": percentual,
                "faixa_probabilidade": (
                    interpretacao_probabilidade["nivel"]
                ),
            }
        )