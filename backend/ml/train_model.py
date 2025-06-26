import os
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
import joblib

# Chemin vers le répertoire racine du projet
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Chemin vers les données
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "accidents_ml.csv")

# Chemin pour sauvegarder le modèle
MODEL_DIR = os.path.join(PROJECT_ROOT, "backend", "ml")
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, "model_gbt.pkl")

print(f"🔄 Chargement des données depuis: {DATA_PATH}")

# 1. Charger les données
df = pd.read_csv(DATA_PATH)
print(f"✅ Données chargées: {len(df)} lignes")

# 2. Séparer les features et la cible
X = df.drop(columns=["target"])  # Assurez-vous que la colonne cible est 'target'
y = df["target"]

# Sauvegarder les noms des colonnes
columns_path = os.path.join(MODEL_DIR, "feature_columns.txt")
with open(columns_path, 'w') as f:
    f.write('\n'.join(X.columns))
print(f"✅ Noms des colonnes sauvegardés: {columns_path}")

# 3. Entraîner le modèle
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = GradientBoostingClassifier(n_estimators=100, random_state=42)

print("🔄 Entraînement du modèle...")
model.fit(X_train, y_train)

# 4. Évaluer le modèle
score = model.score(X_test, y_test)
print(f"✅ Précision sur les données de test: {score:.4f}")

# 5. Sauvegarder le modèle
joblib.dump(model, MODEL_PATH)
print(f"✅ Modèle sauvegardé: {MODEL_PATH}")