from pathlib import Path
import os
import joblib
import xgboost as xgb

# ==========================================
# CAMINHOS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"

PKL_PATH = MODELS_DIR / "modelo_xgboost_final.pkl"
UBJ_PATH = MODELS_DIR / "modelo_xgboost_final.ubj"

print("=" * 70)
print("DIAGNÓSTICO DO MODELO XGBOOST")
print("=" * 70)

# ==========================================
# TAMANHO DOS ARQUIVOS
# ==========================================

if PKL_PATH.exists():
    print(f"\nPKL encontrado:")
    print(f"  {PKL_PATH.name}")
    print(f"  {(PKL_PATH.stat().st_size / 1024 / 1024):.2f} MB")
else:
    print("\nPKL não encontrado.")

if UBJ_PATH.exists():
    print(f"\nUBJ encontrado:")
    print(f"  {UBJ_PATH.name}")
    print(f"  {(UBJ_PATH.stat().st_size / 1024 / 1024):.2f} MB")
else:
    print("\nUBJ não encontrado.")

# ==========================================
# CARREGA O MODELO
# ==========================================

print("\nCarregando modelo...")

if PKL_PATH.exists():

    modelo = joblib.load(PKL_PATH)

    print("Modelo carregado com sucesso.")
    print(f"Tipo do objeto: {type(modelo)}")

    booster = modelo.get_booster()

else:

    booster = xgb.Booster()
    booster.load_model(str(UBJ_PATH))

    print("Booster carregado diretamente do UBJ.")
    print(f"Tipo do objeto: {type(booster)}")

# ==========================================
# INFORMAÇÕES DO BOOSTER
# ==========================================

print("\nInformações do Booster")

try:
    print(f"Número de árvores: {booster.num_boosted_rounds()}")
except Exception as e:
    print(f"Não foi possível obter o número de árvores: {e}")

try:
    print(f"Número de features: {len(booster.feature_names)}")
except Exception:
    pass

try:
    print("\nFeatures:")
    print(booster.feature_names)
except Exception:
    pass

# ==========================================
# TESTE DE NOVO SALVAMENTO
# ==========================================

novo_modelo = MODELS_DIR / "teste_modelo.ubj"

print("\nSalvando novo arquivo UBJ...")

booster.save_model(str(novo_modelo))

print("Arquivo salvo.")

print(
    f"Tamanho do novo UBJ: "
    f"{novo_modelo.stat().st_size / 1024 / 1024:.2f} MB"
)

print("\nDiagnóstico concluído.")
print("=" * 70)