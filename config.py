"""
config.py

Configurações gerais da aplicação.
"""

from services.loader import load_artifacts

# ======================================================
# CARREGA O MODELO UMA ÚNICA VEZ
# ======================================================

ARTIFACTS = load_artifacts()

# ======================================================
# CONFIGURAÇÕES DA APLICAÇÃO
# ======================================================

APP_NAME = "Sistema Inteligente de Predição de Gravidade de Acidentes"

PAGE_TITLE = "Predição de Acidentes"

PAGE_ICON = "🚧"

LAYOUT = "wide"

# ======================================================
# CAMPOS DO FORMULÁRIO
# ======================================================

FIELDS = {

    "uf": "UF",

    "br": "Rodovia (BR)",

    "km": "Quilômetro",

    "ano": "Ano",

    "dia_semana": "Dia da semana",

    "fase_dia": "Fase do dia",

    "sentido_via": "Sentido da via",

    "condicao_metereologica": "Condição meteorológica",

    "tipo_pista": "Tipo de pista",

    "uso_solo": "Perímetro Urbano",

    "tipo_veiculo": "Tipo de veículo",

    "frota": "Frota Municípal",

    "tracado_via": "Traçado da via"

}

# ======================================================
# OPÇÕES DOS SELECTBOX
# ======================================================

OPTIONS = {

    "uf": ARTIFACTS["categories"]["uf"],

    "br": ARTIFACTS["categories"]["br"],

    "ano": ARTIFACTS["categories"]["ano"],

    "dia_semana": ARTIFACTS["categories"]["dia_semana"],

    "fase_dia": ARTIFACTS["categories"]["fase_dia"],

    "sentido_via": ARTIFACTS["categories"]["sentido_via"],

    "condicao_metereologica": ARTIFACTS["categories"]["condicao_metereologica"],

    "tipo_pista": ARTIFACTS["categories"]["tipo_pista"],

    "uso_solo": ARTIFACTS["categories"]["uso_solo"],

    "tipo_veiculo": ARTIFACTS["categories"]["tipo_veiculo"],

}

# ======================================================
# TRAÇADOS
# ======================================================

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

    "Viaduto"

]