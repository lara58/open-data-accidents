from flask import jsonify
import os
import joblib
import pandas as pd
import traceback
from datetime import datetime

from models.prediction_model import save_prediction, get_predictions, get_predictions_by_user
from models.accident_model import get_accident_by_id
from utils.mappings import accident_to_prediction_format

# Chemin vers le modèle
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ml")
MODEL_PATH = os.path.join(MODEL_DIR, "model_gbt.pkl")
COLUMNS_PATH = os.path.join(MODEL_DIR, "feature_columns.txt")

# Variables globales
model = None
feature_columns = []

# Chargement du modèle
try:
    print(f"📁 Chargement du modèle scikit-learn: {MODEL_PATH}")
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        
        if os.path.exists(COLUMNS_PATH):
            with open(COLUMNS_PATH, 'r') as f:
                feature_columns = [line.strip() for line in f.readlines()]
            print(f"✅ Modèle chargé avec succès!")
            print(f"✅ {len(feature_columns)} colonnes chargées.")
        else:
            print("⚠️ Fichier des colonnes introuvable.")
    else:
        print("⚠️ Fichier modèle introuvable. Veuillez exécuter 'python ml/train_model.py' d'abord.")
except Exception as e:
    print(f"❌ Erreur lors du chargement du modèle: {str(e)}")
    traceback.print_exc()

def is_model_loaded():
    """Vérifie si le modèle est disponible"""
    return model is not None

def predict_from_data(data, user_id=None):
    """
    Prédit à partir des données et sauvegarde le résultat
    """
    try:
        if not is_model_loaded():
            print("⚠️ Le modèle n'est pas chargé, impossible de faire une prédiction")
            return None
            
        # Créer une copie des données pour éviter de les modifier
        input_data = {}
        
        # Filtrer et convertir les champs attendus par le modèle
        for col in feature_columns:
            input_data[col] = float(data.get(col, 0))
        
        # Créer un DataFrame avec une seule ligne
        df = pd.DataFrame([input_data])
        
        # Assurer que les colonnes sont dans le bon ordre
        df = df[feature_columns]
        
        # Prédiction
        prediction_class = model.predict(df)[0]
        prediction_proba = model.predict_proba(df)[0]
        
        # Probabilité de la classe prédite
        probability = prediction_proba[prediction_class]
        
        # Convertir en texte
        severity = "Grave" if prediction_class == 1 else "Léger"
        
        # Créer l'objet prédiction avec les champs nécessaires
        prediction = {
            'date_prediction': datetime.now().isoformat(),
            'severity': severity,
            'probability': round(float(probability), 3),
            'dep': int(data.get('dep', 0)),
            'agg': int(data.get('agg', 0)),
            'circ': int(data.get('circ', 0)),
            'atm': int(data.get('atm', 0)),
            'lum': int(data.get('lum', 0)),
            'catv': int(data.get('catv', 0)),
            'catu': int(data.get('catu', 0)),
            'age': int(data.get('age', 0)),
            'trajet': int(data.get('trajet', 0)),
            'secu1': int(data.get('secu1', 0)),
            'place': int(data.get('place', 0)),
            'sexe': int(data.get('sexe', 0)),
            'manv': int(data.get('manv', 0)),
            'motor': int(data.get('motor', 0)),
            'vma': int(data.get('vma', 0)),
            'choc': int(data.get('choc', 0)),
            'latitude': data.get('latitude', None),
            'longitude': data.get('longitude', None),
        }
        
        # Ajouter l'ID utilisateur si fourni
        if user_id:
            prediction['user_id'] = user_id
        
        # Ajouter l'ID de l'accident si fourni
        if 'accident_id' in data:
            prediction['accident_id'] = data['accident_id']
            
        # Sauvegarder en base de données
        prediction_id = save_prediction(prediction)
        prediction['id'] = prediction_id
        
        return prediction
        
    except Exception as e:
        print(f"❌ Erreur lors de la prédiction: {str(e)}")
        traceback.print_exc()
        return None

def predict_from_accident(accident_id, user_id=None):
    """
    Récupère les données d'un accident existant et effectue une prédiction
    """
    try:
        # Récupérer l'accident
        accident = get_accident_by_id(accident_id)
        if not accident:
            print(f"❌ Accident non trouvé avec l'ID: {accident_id}")
            return None
        
        # Convertir au format de prédiction
        prediction_data = accident_to_prediction_format(accident)
        
        # Ajouter l'ID de l'accident pour référence
        prediction_data['accident_id'] = accident_id
        
        # Effectuer la prédiction
        return predict_from_data(prediction_data, user_id)
        
    except Exception as e:
        print(f"❌ Erreur lors de la prédiction depuis accident: {str(e)}")
        traceback.print_exc()
        return None

def list_predictions():
    """
    Récupère toutes les prédictions de la base de données
    """
    try:
        predictions = get_predictions()
        
        # Formater les timestamps pour le frontend
        for prediction in predictions:
            if 'date_prediction' in prediction and prediction['date_prediction']:
                if isinstance(prediction['date_prediction'], str):
                    # Déjà formaté en chaîne
                    pass
                else:
                    # Convertir en ISO format
                    prediction['date_prediction'] = prediction['date_prediction'].isoformat()
                    
        return predictions
    except Exception as e:
        print(f"❌ Erreur dans list_predictions: {str(e)}")
        traceback.print_exc()
        return []

def list_user_predictions(user_id):
    """
    Récupère les prédictions d'un utilisateur spécifique
    """
    try:
        if not user_id:
            return []
            
        predictions = get_predictions_by_user(user_id)
        
        # Formater les timestamps pour le frontend
        for prediction in predictions:
            if 'date_prediction' in prediction and prediction['date_prediction']:
                if isinstance(prediction['date_prediction'], str):
                    # Déjà formaté en chaîne
                    pass
                else:
                    # Convertir en ISO format
                    prediction['date_prediction'] = prediction['date_prediction'].isoformat()
                    
        return predictions
    except Exception as e:
        print(f"❌ Erreur dans list_user_predictions: {str(e)}")
        traceback.print_exc()
        return []