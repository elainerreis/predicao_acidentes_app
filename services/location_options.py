"""
location_options.py

Funções auxiliares para tratamento das
opções de localização, ordenação de
categorias e navegação entre quilômetros
válidos.
"""

from typing import Any


def ordenar_brs(brs: list[str]) -> list[str]:
    def chave(valor: str) -> tuple[int, float | str]:
        try:
            return 0, float(valor)
        except (TypeError, ValueError):
            return 1, str(valor)

    return sorted(brs, key=chave)


def formatar_br(valor: str) -> str:
    try:
        return f"BR-{int(float(valor)):03d}"
    except (TypeError, ValueError):
        return str(valor)


def primeiro_km(intervalos: list[list[int]]) -> int:
    if not intervalos:
        return 0

    return int(intervalos[0][0])


def ultimo_km(intervalos: list[list[int]]) -> int:
    if not intervalos:
        return 0

    return int(intervalos[-1][1])


def proximo_km(
    km_atual: int,
    intervalos: list[list[int]],
) -> int:
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


def ordenar_opcoes(
    opcoes_disponiveis: list[Any],
    ordem_preferencial: list[str],
) -> list[Any]:
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

    incluidos = {
        str(opcao)
        for opcao in ordenadas
    }

    restantes = [
        opcao
        for opcao in opcoes
        if str(opcao) not in incluidos
    ]

    return ordenadas + sorted(
        restantes,
        key=lambda valor: str(valor),
    )


def obter_ordem_exibicao(
    metadata: dict[str, Any],
    variavel: str,
    ordem_padrao: list[str],
) -> list[str]:
    ordem = (
        metadata
        .get("display_order", {})
        .get(variavel)
    )

    if ordem:
        return list(ordem)

    if variavel == "dia_semana":
        ordem_antiga = metadata.get("days_order")

        if ordem_antiga:
            return list(ordem_antiga)

    return ordem_padrao