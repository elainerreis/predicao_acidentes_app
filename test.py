import joblib

metadata = joblib.load(
    "models/amostra_metadata.pkl"
)

print(
    metadata["location_intervals"]["ES"]["447.0"]
)