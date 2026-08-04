"""
dashboard_analysis.py

Gera interpretações automáticas para as visualizações
da página de análise exploratória.
"""

from html import escape

import pandas as pd
import streamlit as st


def _formatar_inteiro(valor: int) -> str:
    """Formata números inteiros com separador de milhar brasileiro."""

    return f"{int(valor):,}".replace(",", ".")


def _formatar_percentual(valor: float) -> str:
    """Formata percentuais com uma casa decimal."""

    return f"{valor:.1f}".replace(".", ",") + "%"


def _formatar_br(valor) -> str:
    """
    Padroniza o nome da rodovia.

    Exemplos:
        40 -> BR-040
        101.0 -> BR-101
        BR-116 -> BR-116
    """

    valor = str(valor).strip().replace(".0", "")

    if valor.upper().startswith("BR-"):
        numero = valor[3:]
    elif valor.upper().startswith("BR"):
        numero = valor[2:].replace("-", "").strip()
    else:
        numero = valor

    if numero.isdigit():
        numero = numero.zfill(3)

    return f"BR-{numero}"


def _contagem_categoria(
    df: pd.DataFrame,
    coluna: str,
) -> pd.Series:
    """
    Retorna a contagem de registros por categoria,
    desconsiderando valores ausentes ou vazios.
    """

    if coluna not in df.columns:
        return pd.Series(dtype="int64")

    serie = df[coluna].copy()

    serie = serie.dropna()
    serie = serie.astype(str).str.strip()

    serie = serie[
        ~serie.isin(
            [
                "",
                "nan",
                "None",
                "<NA>",
            ]
        )
    ]

    return serie.value_counts()


def show_location_analysis(df: pd.DataFrame) -> None:
    """
    Exibe uma interpretação automática da distribuição
    dos registros por UF e BR.
    """

    if df is None or df.empty:
        st.info(
            "Não há dados suficientes para gerar a análise de localização."
        )
        return

    total_registros = len(df)

    contagem_uf = _contagem_categoria(
        df=df,
        coluna="uf",
    )

    contagem_br = _contagem_categoria(
        df=df,
        coluna="br",
    )

    if contagem_uf.empty and contagem_br.empty:
        st.info(
            "As variáveis de localização não estão disponíveis "
            "para o conjunto de dados selecionado."
        )
        return

    observacoes = []

    # ==================================================
    # ANÁLISE DE FREQUÊNCIA E GRAVIDADE POR UF
    # ==================================================

    analise_gravidade_uf = pd.DataFrame()

    if {"uf", "gravidade"}.issubset(df.columns):
        df_gravidade = df[["uf", "gravidade"]].copy()

        df_gravidade = df_gravidade.dropna(subset=["uf", "gravidade"])

        df_gravidade["uf"] = (
            df_gravidade["uf"]
            .astype(str)
            .str.strip()
        )

        df_gravidade["gravidade"] = pd.to_numeric(
            df_gravidade["gravidade"],
            errors="coerce",
        )

        df_gravidade = df_gravidade.dropna(
            subset=["gravidade"]
        )

        df_gravidade = df_gravidade[
            ~df_gravidade["uf"].isin(
                ["", "nan", "None", "<NA>"]
            )
        ]

        if not df_gravidade.empty:
            analise_gravidade_uf = (
                df_gravidade
                .groupby("uf", as_index=False)
                .agg(
                    total_registros=("gravidade", "size"),
                    total_graves=("gravidade", "sum"),
                    taxa_gravidade=("gravidade", "mean"),
                )
            )

    # ==================================================
    # ANÁLISE POR UF
    # ==================================================

    if not contagem_uf.empty:
        principal_uf = escape(str(contagem_uf.index[0]))
        quantidade_uf = int(contagem_uf.iloc[0])

        percentual_uf = (
            quantidade_uf / total_registros
        ) * 100

        quantidade_top_5_uf = int(
            contagem_uf.head(5).sum()
        )

        percentual_top_5_uf = (
            quantidade_top_5_uf / total_registros
        ) * 100

        observacoes.append(
            f"""
            A unidade da federação com maior número de registros foi
            <strong>{principal_uf}</strong>, com
            <strong>{_formatar_inteiro(quantidade_uf)}</strong>
            pessoas envolvidas, correspondendo a
            <strong>{_formatar_percentual(percentual_uf)}</strong>
            do conjunto atualmente selecionado.
            """
        )

        if len(contagem_uf) >= 5:
            observacoes.append(
                f"""
                As cinco unidades da federação com maior frequência
                concentraram
                <strong>{_formatar_percentual(percentual_top_5_uf)}</strong>
                dos registros filtrados.
                """
            )

    # ==================================================
    # ANÁLISE POR BR
    # ==================================================

    if not contagem_br.empty:
        principal_br = _formatar_br(
            contagem_br.index[0]
        )

        quantidade_br = int(contagem_br.iloc[0])

        percentual_br = (
            quantidade_br / total_registros
        ) * 100

        observacoes.append(
            f"""
            Entre as rodovias, a
            <strong>{escape(principal_br)}</strong>
            apresentou a maior frequência, com
            <strong>{_formatar_inteiro(quantidade_br)}</strong>
            registros, equivalentes a
            <strong>{_formatar_percentual(percentual_br)}</strong>
            do total analisado.
            """
        )

    # ==================================================
    # INTERPRETAÇÃO DO SCATTER
    # ==================================================

    if not analise_gravidade_uf.empty:
        taxa_media_geral = (
            analise_gravidade_uf["total_graves"].sum()
            / analise_gravidade_uf["total_registros"].sum()
        )

        uf_maior_taxa = analise_gravidade_uf.loc[
            analise_gravidade_uf["taxa_gravidade"].idxmax()
        ]

        observacoes.append(
            f"""
            A taxa média de gravidade no recorte analisado foi de
            <strong>
                {_formatar_percentual(taxa_media_geral * 100)}
            </strong>.
            A maior taxa entre as unidades da federação foi observada em
            <strong>{escape(str(uf_maior_taxa["uf"]))}</strong>,
            com
            <strong>
                {_formatar_percentual(
                    float(uf_maior_taxa["taxa_gravidade"]) * 100
                )}
            </strong>.
            """
        )

        ufs_acima_media = analise_gravidade_uf[
            analise_gravidade_uf["taxa_gravidade"]
            > taxa_media_geral
        ]

        if not ufs_acima_media.empty:
            uf_destaque = ufs_acima_media.loc[
                ufs_acima_media["total_registros"].idxmax()
            ]

            observacoes.append(
                f"""
                Entre as unidades da federação com taxa de gravidade
                acima da média, <strong>
                {escape(str(uf_destaque["uf"]))}</strong>
                apresentou o maior volume de registros, com
                <strong>
                    {_formatar_inteiro(
                        int(uf_destaque["total_registros"])
                    )}
                </strong>
                pessoas envolvidas.
                """
            )

    texto_observacoes = "".join(
        f'<p class="analysis-text">{texto}</p>'
        for texto in observacoes
    )

    st.html(
        f"""
        <article class="analysis-card">
            <p class="analysis-label">
                LEITURA DOS DADOS
            </p>

            <h3 class="analysis-title">
                Distribuição geográfica e gravidade
            </h3>

            {texto_observacoes}

            <p class="analysis-note">
                A frequência representa o número de pessoas envolvidas nos
                registros selecionados. A taxa de gravidade corresponde à
                proporção de pessoas com lesões graves ou óbito. Essas medidas
                devem ser interpretadas em conjunto.
            </p>
        </article>
        """
    )

def show_time_analysis(df: pd.DataFrame) -> None:
    """
    Exibe uma interpretação automática da distribuição temporal
    dos registros selecionados.
    """

    if df is None or df.empty:
        st.info(
            "Não há dados suficientes para gerar a análise temporal."
        )
        return

    total_registros = len(df)
    observacoes = []

    contagem_ano = _contagem_categoria(
        df=df,
        coluna="ano",
    )

    contagem_dia = _contagem_categoria(
        df=df,
        coluna="dia_semana",
    )

    contagem_fase = _contagem_categoria(
        df=df,
        coluna="fase_dia",
    )

    # ==================================================
    # ANO
    # ==================================================

    if not contagem_ano.empty:
        principal_ano = escape(str(contagem_ano.index[0]))
        quantidade_ano = int(contagem_ano.iloc[0])

        percentual_ano = (
            quantidade_ano / total_registros
        ) * 100

        observacoes.append(
            f"""
            O ano com maior número de registros no recorte selecionado
            foi <strong>{principal_ano}</strong>, com
            <strong>{_formatar_inteiro(quantidade_ano)}</strong>
            pessoas envolvidas, equivalentes a
            <strong>{_formatar_percentual(percentual_ano)}</strong>
            do total analisado.
            """
        )

    # ==================================================
    # DIA DA SEMANA
    # ==================================================

    if not contagem_dia.empty:
        principal_dia = escape(str(contagem_dia.index[0]))
        quantidade_dia = int(contagem_dia.iloc[0])

        percentual_dia = (
            quantidade_dia / total_registros
        ) * 100

        observacoes.append(
            f"""
            O dia da semana com maior frequência foi
            <strong>{principal_dia}</strong>, reunindo
            <strong>{_formatar_inteiro(quantidade_dia)}</strong>
            registros, ou
            <strong>{_formatar_percentual(percentual_dia)}</strong>
            do conjunto filtrado.
            """
        )

    # ==================================================
    # FASE DO DIA
    # ==================================================

    if not contagem_fase.empty:
        principal_fase = escape(str(contagem_fase.index[0]))
        quantidade_fase = int(contagem_fase.iloc[0])

        percentual_fase = (
            quantidade_fase / total_registros
        ) * 100

        observacoes.append(
            f"""
            A fase do dia mais recorrente foi
            <strong>{principal_fase}</strong>, com
            <strong>{_formatar_inteiro(quantidade_fase)}</strong>
            registros, correspondendo a
            <strong>{_formatar_percentual(percentual_fase)}</strong>
            do total analisado.
            """
        )

    # ==================================================
    # DIA DA SEMANA × FASE DO DIA
    # ==================================================

    if {"dia_semana", "fase_dia"}.issubset(df.columns):
        df_combinacao = df[
            ["dia_semana", "fase_dia"]
        ].copy()

        df_combinacao = df_combinacao.dropna()

        df_combinacao["dia_semana"] = (
            df_combinacao["dia_semana"]
            .astype(str)
            .str.strip()
        )

        df_combinacao["fase_dia"] = (
            df_combinacao["fase_dia"]
            .astype(str)
            .str.strip()
        )

        valores_invalidos = [
            "",
            "nan",
            "None",
            "<NA>",
        ]

        df_combinacao = df_combinacao[
            ~df_combinacao["dia_semana"].isin(
                valores_invalidos
            )
            & ~df_combinacao["fase_dia"].isin(
                valores_invalidos
            )
        ]

        if not df_combinacao.empty:
            combinacoes = (
                df_combinacao
                .value_counts(
                    ["dia_semana", "fase_dia"]
                )
                .reset_index(name="quantidade")
            )

            principal_combinacao = combinacoes.iloc[0]

            dia_combinacao = escape(
                str(principal_combinacao["dia_semana"])
            )

            fase_combinacao = escape(
                str(principal_combinacao["fase_dia"])
            )

            quantidade_combinacao = int(
                principal_combinacao["quantidade"]
            )

            percentual_combinacao = (
                quantidade_combinacao / total_registros
            ) * 100

            observacoes.append(
                f"""
                A combinação temporal mais frequente foi
                <strong>{dia_combinacao}</strong> durante
                <strong>{fase_combinacao}</strong>, com
                <strong>
                    {_formatar_inteiro(quantidade_combinacao)}
                </strong>
                registros, equivalentes a
                <strong>
                    {_formatar_percentual(percentual_combinacao)}
                </strong>
                do recorte selecionado.
                """
            )

    if not observacoes:
        st.info(
            "As variáveis temporais não estão disponíveis "
            "para o conjunto de dados selecionado."
        )
        return

    texto_observacoes = "".join(
        f'<p class="analysis-text">{texto}</p>'
        for texto in observacoes
    )

    st.html(
        f"""
        <article class="analysis-card">
            <p class="analysis-label">
                LEITURA DOS DADOS
            </p>

            <h3 class="analysis-title">
                Distribuição temporal
            </h3>

            {texto_observacoes}

            <p class="analysis-note">
                As frequências apresentadas refletem o recorte
                selecionado pelos filtros. Elas descrevem a
                concentração dos registros, mas não representam,
                isoladamente, maior risco de ocorrência.
            </p>
        </article>
        """
    )

def show_conditions_analysis(df: pd.DataFrame) -> None:
    """
    Exibe uma interpretação automática das condições da via
    e do ambiente no recorte selecionado.
    """

    if df is None or df.empty:
        st.info(
            "Não há dados suficientes para gerar a análise "
            "das condições dos acidentes."
        )
        return

    total_registros = len(df)
    observacoes = []

    # ==================================================
    # TIPO DE PISTA
    # ==================================================

    contagem_tipo_pista = _contagem_categoria(
        df=df,
        coluna="tipo_pista",
    )

    if not contagem_tipo_pista.empty:
        principal_tipo_pista = escape(
            str(contagem_tipo_pista.index[0])
        )

        quantidade_tipo_pista = int(
            contagem_tipo_pista.iloc[0]
        )

        percentual_tipo_pista = (
            quantidade_tipo_pista / total_registros
        ) * 100

        observacoes.append(
            f"""
            O tipo de pista mais frequente foi
            <strong>{principal_tipo_pista}</strong>, presente em
            <strong>
                {_formatar_inteiro(quantidade_tipo_pista)}
            </strong>
            registros, o que corresponde a
            <strong>
                {_formatar_percentual(percentual_tipo_pista)}
            </strong>
            do recorte selecionado.
            """
        )

    # ==================================================
    # CONDIÇÃO METEOROLÓGICA
    # ==================================================

    contagem_clima = _contagem_categoria(
        df=df,
        coluna="condicao_metereologica",
    )

    if not contagem_clima.empty:
        principal_clima = escape(
            str(contagem_clima.index[0])
        )

        quantidade_clima = int(
            contagem_clima.iloc[0]
        )

        percentual_clima = (
            quantidade_clima / total_registros
        ) * 100

        observacoes.append(
            f"""
            A condição meteorológica predominante foi
            <strong>{principal_clima}</strong>, associada a
            <strong>
                {_formatar_inteiro(quantidade_clima)}
            </strong>
            registros, equivalentes a
            <strong>
                {_formatar_percentual(percentual_clima)}
            </strong>
            do total analisado.
            """
        )

    # ==================================================
    # PERÍMETRO URBANO
    # ==================================================

    contagem_perimetro = _contagem_categoria(
        df=df,
        coluna="uso_solo",
    )

    if not contagem_perimetro.empty:
        principal_perimetro = escape(
            str(contagem_perimetro.index[0])
        )

        quantidade_perimetro = int(
            contagem_perimetro.iloc[0]
        )

        percentual_perimetro = (
            quantidade_perimetro / total_registros
        ) * 100

        observacoes.append(
            f"""
            Em relação ao perímetro urbano, a categoria mais recorrente foi
            <strong>{principal_perimetro}</strong>, com
            <strong>
                {_formatar_inteiro(quantidade_perimetro)}
            </strong>
            registros, representando
            <strong>
                {_formatar_percentual(percentual_perimetro)}
            </strong>
            do conjunto filtrado.
            """
        )

    # ==================================================
    # TRAÇADO DA VIA
    # ==================================================

    colunas_tracado = [
        "Reta",
        "Curva",
        "Declive",
        "Aclive",
        "Interseção de Vias",
        "Em Obras",
        "Retorno Regulamentado",
        "Rotatória",
        "Ponte",
        "Viaduto",
        "Desvio Temporário",
        "Túnel",
    ]

    colunas_disponiveis = [
        coluna
        for coluna in colunas_tracado
        if coluna in df.columns
    ]

    if colunas_disponiveis:
        totais_tracado = {}

        for coluna in colunas_disponiveis:
            valores = pd.to_numeric(
                df[coluna],
                errors="coerce",
            ).fillna(0)

            totais_tracado[coluna] = int(
                valores.sum()
            )

        totais_tracado = pd.Series(
            totais_tracado,
            dtype="int64",
        ).sort_values(ascending=False)

        totais_tracado = totais_tracado[
            totais_tracado > 0
        ]

        if not totais_tracado.empty:
            principal_tracado = escape(
                str(totais_tracado.index[0])
            )

            quantidade_tracado = int(
                totais_tracado.iloc[0]
            )

            percentual_tracado = (
                quantidade_tracado / total_registros
            ) * 100

            observacoes.append(
                f"""
                Entre as características do traçado da via,
                <strong>{principal_tracado}</strong> apresentou a
                maior ocorrência, estando presente em
                <strong>
                    {_formatar_inteiro(quantidade_tracado)}
                </strong>
                registros, ou
                <strong>
                    {_formatar_percentual(percentual_tracado)}
                </strong>
                do recorte selecionado.
                """
            )

    # ==================================================
    # EXIBIÇÃO
    # ==================================================

    if not observacoes:
        st.info(
            "As variáveis relacionadas às condições da via "
            "e do ambiente não estão disponíveis."
        )
        return

    texto_observacoes = "".join(
        f'<p class="analysis-text">{texto}</p>'
        for texto in observacoes
    )

    st.html(
        f"""
        <article class="analysis-card">
            <p class="analysis-label">
                LEITURA DOS DADOS
            </p>

            <h3 class="analysis-title">
                Condições da via e do ambiente
            </h3>

            {texto_observacoes}

            <p class="analysis-note">
                As frequências representam características presentes
                nos registros selecionados. Uma categoria com maior
                ocorrência não deve ser interpretada isoladamente
                como causa do acidente ou como indicação direta de
                maior risco.
            </p>
        </article>
        """
    )

def show_vehicle_analysis(df: pd.DataFrame) -> None:
    """
    Exibe uma interpretação automática sobre os tipos
    de veículo envolvidos nos registros selecionados.
    """

    if df is None or df.empty:
        st.info(
            "Não há dados suficientes para gerar a análise "
            "do perfil dos veículos."
        )
        return

    contagem_veiculos = _contagem_categoria(
        df=df,
        coluna="tipo_veiculo",
    )

    if contagem_veiculos.empty:
        st.info(
            "A variável de tipo de veículo não está disponível "
            "para o recorte selecionado."
        )
        return

    total_registros = int(contagem_veiculos.sum())

    principal_veiculo = escape(
        str(contagem_veiculos.index[0])
    )

    quantidade_principal = int(
        contagem_veiculos.iloc[0]
    )

    percentual_principal = (
        quantidade_principal / total_registros
    ) * 100 if total_registros > 0 else 0

    observacoes = [
        f"""
        O tipo de veículo com maior número de pessoas envolvidas foi
        <strong>{principal_veiculo}</strong>, com
        <strong>{_formatar_inteiro(quantidade_principal)}</strong>
        registros, correspondendo a
        <strong>{_formatar_percentual(percentual_principal)}</strong>
        do total analisado.
        """
    ]

    # Segundo tipo de veículo mais frequente
    if len(contagem_veiculos) > 1:
        segundo_veiculo = escape(
            str(contagem_veiculos.index[1])
        )

        quantidade_segundo = int(
            contagem_veiculos.iloc[1]
        )

        percentual_segundo = (
            quantidade_segundo / total_registros
        ) * 100 if total_registros > 0 else 0

        observacoes.append(
            f"""
            Em seguida aparece
            <strong>{segundo_veiculo}</strong>, com
            <strong>{_formatar_inteiro(quantidade_segundo)}</strong>
            registros, equivalentes a
            <strong>{_formatar_percentual(percentual_segundo)}</strong>
            do conjunto filtrado.
            """
        )

    texto_observacoes = "".join(
        f'<p class="analysis-text">{texto}</p>'
        for texto in observacoes
    )

    st.html(
        f"""
        <article class="analysis-card">
            <p class="analysis-label">
                LEITURA DOS DADOS
            </p>

            <h3 class="analysis-title">
                Perfil dos veículos envolvidos
            </h3>

            {texto_observacoes}

            <p class="analysis-note">
                A frequência representa o número de pessoas associadas
                a cada tipo de veículo nos registros selecionados.
                Como a base está organizada por pessoa acidentada,
                esses valores não correspondem diretamente ao número
                de veículos ou ao número de acidentes.
            </p>
        </article>
        """
    )