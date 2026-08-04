"""
predict.py

Página destinada à simulação da gravidade de acidentes
em rodovias federais brasileiras.
"""

from typing import Any

import streamlit as st

from config import FIELDS, OPTIONS, TRACADOS
from services.loader import load_metadata
from services.predictor import predict
from components.predict_analysis import show_prediction
from components.predict_hero import show_prediction_hero


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def ordenar_brs(brs: list[str]) -> list[str]:
    """Ordena as BRs pelo valor numérico."""

    def chave(valor: str) -> tuple[int, float | str]:
        try:
            return 0, float(valor)
        except (TypeError, ValueError):
            return 1, str(valor)

    return sorted(brs, key=chave)


def formatar_br(valor: str) -> str:
    """
    Formata a BR somente para exibição.

    O valor original continua sendo enviado ao modelo.
    """

    try:
        return f"BR-{int(float(valor)):03d}"
    except (TypeError, ValueError):
        return str(valor)


def ordenar_opcoes(
    opcoes_disponiveis: list[Any],
    ordem_preferencial: list[str],
) -> list[Any]:
    """Ordena as categorias conforme a ordem definida no metadata."""

    opcoes = list(opcoes_disponiveis)

    mapa_opcoes = {
        str(opcao): opcao
        for opcao in opcoes
    }

    ordenadas = [
        mapa_opcoes[valor]
        for valor in ordem_preferencial
        if valor in mapa_opcoes
    ]

    textos_incluidos = {
        str(opcao)
        for opcao in ordenadas
    }

    restantes = [
        opcao
        for opcao in opcoes
        if str(opcao) not in textos_incluidos
    ]

    restantes = sorted(
        restantes,
        key=lambda valor: str(valor),
    )

    return ordenadas + restantes


def obter_ordem_exibicao(
    metadata: dict[str, Any],
    variavel: str,
    ordem_padrao: list[str],
) -> list[str]:
    """Recupera a ordem da variável armazenada no metadata."""

    ordem = (
        metadata
        .get("display_order", {})
        .get(variavel)
    )

    if ordem:
        return list(ordem)

    # Compatibilidade com a versão anterior do metadata.
    if variavel == "dia_semana":
        ordem_antiga = metadata.get("days_order")

        if ordem_antiga:
            return list(ordem_antiga)

    return ordem_padrao


def primeiro_km(intervalos: list[list[int]]) -> int:
    """Retorna o primeiro KM válido."""

    if not intervalos:
        return 0

    return int(intervalos[0][0])


def ultimo_km(intervalos: list[list[int]]) -> int:
    """Retorna o último KM válido."""

    if not intervalos:
        return 0

    return int(intervalos[-1][1])


def proximo_km(
    km_atual: int,
    intervalos: list[list[int]],
) -> int:
    """
    Retorna o próximo KM válido.

    Quando chega ao fim de um intervalo, salta para
    o início do intervalo seguinte.
    """

    if not intervalos:
        return 0

    km_atual = int(km_atual)

    for inicio, fim in intervalos:
        inicio = int(inicio)
        fim = int(fim)

        if inicio <= km_atual < fim:
            return km_atual + 1

        if km_atual < inicio:
            return inicio

    return ultimo_km(intervalos)


def km_anterior(
    km_atual: int,
    intervalos: list[list[int]],
) -> int:
    """
    Retorna o KM válido anterior.

    Quando chega ao início de um intervalo, salta para
    o final do intervalo anterior.
    """

    if not intervalos:
        return 0

    km_atual = int(km_atual)

    for inicio, fim in reversed(intervalos):
        inicio = int(inicio)
        fim = int(fim)

        if inicio < km_atual <= fim:
            return km_atual - 1

        if km_atual > fim:
            return fim

    return primeiro_km(intervalos)


def atualizar_km_anterior(
    chave_km: str,
    intervalos: list[list[int]],
) -> None:
    """Callback do botão de KM anterior."""

    valor_atual = int(
        st.session_state.get(
            chave_km,
            primeiro_km(intervalos),
        )
    )

    st.session_state[chave_km] = km_anterior(
        km_atual=valor_atual,
        intervalos=intervalos,
    )


def atualizar_proximo_km(
    chave_km: str,
    intervalos: list[list[int]],
) -> None:
    """Callback do botão de próximo KM."""

    valor_atual = int(
        st.session_state.get(
            chave_km,
            primeiro_km(intervalos),
        )
    )

    st.session_state[chave_km] = proximo_km(
        km_atual=valor_atual,
        intervalos=intervalos,
    )

def limpar_kms_armazenados() -> None:
    """
    Remove os valores de KM armazenados quando a UF
    ou a BR é alterada.
    """

    chaves_km = [
        chave
        for chave in st.session_state
        if chave.startswith("prediction_km_")
    ]

    for chave in chaves_km:
        del st.session_state[chave]


def atualizar_dependencias_uf() -> None:
    """
    Reinicia a BR e o KM quando a UF é alterada.
    """

    st.session_state.pop(
        "prediction_br",
        None,
    )

    limpar_kms_armazenados()


def atualizar_dependencias_br() -> None:
    """
    Reinicia o KM quando a BR é alterada.
    """

    limpar_kms_armazenados()

# =========================================================
# METADATA
# =========================================================

metadata = load_metadata()

location_intervals = metadata.get(
    "location_intervals",
    {},
)

if not location_intervals:
    st.error(
        "O metadata não contém os intervalos de localização."
    )
    st.stop()


# =========================================================
# ORDENAÇÃO DOS CAMPOS
# =========================================================

ordem_dias = obter_ordem_exibicao(
    metadata=metadata,
    variavel="dia_semana",
    ordem_padrao=[
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
    metadata=metadata,
    variavel="fase_dia",
    ordem_padrao=[
        "Plena Noite",
        "Amanhecer",
        "Pleno dia",
        "Anoitecer",
    ],
)

dias_semana_disponiveis = ordenar_opcoes(
    opcoes_disponiveis=OPTIONS["dia_semana"],
    ordem_preferencial=ordem_dias,
)

fases_dia_disponiveis = ordenar_opcoes(
    opcoes_disponiveis=OPTIONS["fase_dia"],
    ordem_preferencial=ordem_fases,
)


# =========================================================
# HERO
# =========================================================

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


# =========================================================
# CONTAINER VISUAL DA PREDIÇÃO
# =========================================================

with st.container(key="prediction_form"):

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

    # UF
    ufs_disponiveis = sorted(
        location_intervals.keys()
    )

    with col_uf:
        uf = st.selectbox(
            label=FIELDS["uf"],
            options=ufs_disponiveis,
            key="prediction_uf",
        )

    # BR filtrada pela UF
    brs_disponiveis = ordenar_brs(
        list(
            location_intervals
            .get(uf, {})
            .keys()
        )
    )

    if not brs_disponiveis:
        st.error(
            f"Nenhuma BR foi encontrada para a UF {uf}."
        )
        st.stop()

    # Remove uma BR pertencente à UF selecionada anteriormente.

    with col_br:
        br = st.selectbox(
            label=FIELDS["br"],
            options=brs_disponiveis,
            format_func=formatar_br,
            key="prediction_br",
        )

    # Intervalos válidos da combinação UF + BR
    intervalos_km = (
        location_intervals
        .get(uf, {})
        .get(br, [])
    )

    if not intervalos_km:
        st.error(
            "Nenhum intervalo de KM foi encontrado para "
            f"{formatar_br(br)} em {uf}."
        )
        st.stop()

    chave_km = f"prediction_km_{uf}_{br}"

    if chave_km not in st.session_state:
        st.session_state[chave_km] = primeiro_km(
            intervalos_km
        )

    # KM com valores válidos
    with col_km:
        col_anterior, col_valor, col_proximo = st.columns(
            [1, 2.4, 1],
            gap="small",
            vertical_alignment="bottom",
        )

        with col_anterior:
            st.button(
                label="−",
                key=f"previous_{uf}_{br}",
                width="stretch",
                help="Ir para o quilômetro válido anterior.",
                on_click=atualizar_km_anterior,
                args=(
                    chave_km,
                    intervalos_km,
                ),
            )

        with col_valor:
            st.number_input(
                label=FIELDS["km"],
                min_value=primeiro_km(intervalos_km),
                max_value=ultimo_km(intervalos_km),
                step=1,
                disabled=True,
                key=chave_km,
                help=(
                    "Apenas quilômetros existentes na base de dados "
                    "para a UF e a BR selecionadas podem ser utilizados. "
                    "Use os botões − e + para navegar entre os valores."
                ),
            )

        with col_proximo:
            st.button(
                label="+",
                key=f"next_{uf}_{br}",
                width="stretch",
                help="Ir para o próximo quilômetro válido.",
                on_click=atualizar_proximo_km,
                args=(
                    chave_km,
                    intervalos_km,
                ),
            )

        km = int(
            st.session_state[chave_km]
        )

    # Frota
    with col_frota:
        frota = st.number_input(
            label=FIELDS["frota"],
            min_value=0.0,
            value=10000.0,
            step=1000.0,
            key="prediction_frota",
            help=(
                "Quantidade total de veículos "
                "registrados no município."
            ),
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
            key="prediction_tipo_pista",
        )

    with col_uso:
        uso_solo = st.selectbox(
            label=FIELDS["uso_solo"],
            options=OPTIONS["uso_solo"],
            key="prediction_uso_solo",
        )

    tracado = st.multiselect(
        label="Traçado da via",
        options=TRACADOS,
        placeholder=(
            "Selecione uma ou mais características do traçado"
        ),
        help=(
            "O trecho pode apresentar mais de uma característica, "
            "como reta, curva, aclive ou interseção."
        ),
        key="prediction_tracado",
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
            key="prediction_ano",
        )

    with col_dia:
        dia_semana = st.selectbox(
            label=FIELDS["dia_semana"],
            options=dias_semana_disponiveis,
            key="prediction_dia_semana",
        )

    with col_fase:
        fase_dia = st.selectbox(
            label=FIELDS["fase_dia"],
            options=fases_dia_disponiveis,
            key="prediction_fase_dia",
        )

    col_condicao, col_sentido = st.columns(
        2,
        gap="medium",
    )

    with col_condicao:
        condicao = st.selectbox(
            label=FIELDS["condicao_metereologica"],
            options=OPTIONS["condicao_metereologica"],
            key="prediction_condicao",
        )

    with col_sentido:
        sentido_via = st.selectbox(
            label=FIELDS["sentido_via"],
            options=OPTIONS["sentido_via"],
            key="prediction_sentido_via",
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
        key="prediction_tipo_veiculo",
    )

    st.markdown("")

    submitted = st.button(
        label="Calcular probabilidade",
        width="stretch",
        type="primary",
        key="prediction_submit",
    )


# =========================================================
# EXECUÇÃO DA PREDIÇÃO
# =========================================================

if submitted:

    dados = {
        "uf": uf,
        "br": br,
        "km": float(km),
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