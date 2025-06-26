# services/predictor.py

# Fonction temporaire de prédiction
# def predire_gravite(data):
#     # future: appel d'un modèle ML
#     if data["vitesse_max"] > 70 or data["agglomeration"] == 0:
#         return 1
#     return 0

import os
import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

# === Chemins globaux ===
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATA_PATH = os.path.join(PROJECT_ROOT, "backend", "data", "accidents_ml.csv")
MODEL_DIR = os.path.join(PROJECT_ROOT, "backend", "ml")
MODEL_PATH = os.path.join(MODEL_DIR, "model_gbt.pkl")
COLUMNS_PATH = os.path.join(MODEL_DIR, "feature_columns.txt")

# === Entraînement du modèle ===
def entrainer_modele():
    os.makedirs(MODEL_DIR, exist_ok=True)
    print(f"📂 Chargement des données depuis: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    print(f"✅ {len(df)} lignes chargées.")

    X = df.drop(columns=["target"])
    y = df["target"]

    # Sauvegarde des colonnes
    with open(COLUMNS_PATH, 'w') as f:
        f.write('\n'.join(X.columns))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = GradientBoostingClassifier(n_estimators=100, random_state=42)

    print("⚙️ Entraînement du modèle...")
    model.fit(X_train, y_train)
    print(f"✅ Score test: {model.score(X_test, y_test):.4f}")

    joblib.dump(model, MODEL_PATH)
    print(f"✅ Modèle sauvegardé dans {MODEL_PATH}")

# === Fonction de prédiction utilisée par l'API ===
def predire_gravite(data):
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Modèle non entraîné. Exécutez entrainer_modele() d'abord.")

    model = joblib.load(MODEL_PATH)

    # Charger les noms de colonnes
    with open(COLUMNS_PATH, 'r') as f:
        colonnes = f.read().splitlines()

    # Réorganiser les données selon l’ordre d’entraînement
    entree = pd.DataFrame([[data[col] for col in colonnes]], columns=colonnes)
    
    print(f"[🧠 Prédiction] Données envoyées au modèle : {data}")
    print(f"[🧠 Prédiction] Colonnes utilisées : {colonnes}")

    print(f"[🧠 Prédiction] DataFrame d'entrée :\n{entree}")

    prediction = model.predict(entree)[0]
    probas = model.predict_proba(entree)[0]  # [proba_non_grave, proba_grave]
    proba_grave = float(probas[1])  # probabilité que l'accident soit grave (classe 1)

    return int(prediction), round(proba_grave * 100, 2)  


# Permet de lancer l'entraînement depuis la ligne de commande
if __name__ == "__main__":
    entrainer_modele()
