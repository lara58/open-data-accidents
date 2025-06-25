from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from datetime import datetime
import traceback

app = Flask(__name__)
CORS(app)  # Activer CORS pour toutes les routes

# Stockage en mémoire pour les prédictions
predictions_history = []
next_id = 1

@app.route('/predictions', methods=['GET'])
def get_predictions():
    """Endpoint pour récupérer l'historique des prédictions"""
    try:
        # Récupérer le nombre de prédictions à afficher
        limit = request.args.get('limit', 10, type=int)
        
        # Retourner les prédictions (triées par date, les plus récentes d'abord)
        sorted_predictions = sorted(
            predictions_history, 
            key=lambda x: x["date_prediction"], 
            reverse=True
        )
        
        return jsonify(sorted_predictions[:limit])
        
    except Exception as e:
        error_msg = f"Erreur lors de la récupération des prédictions: {str(e)}"
        print(f"❌ {error_msg}")
        print(traceback.format_exc())
        return jsonify({"error": error_msg}), 500

@app.route('/save-prediction', methods=['POST'])
def save_prediction():
    """Endpoint pour sauvegarder une prédiction"""
    global next_id
    try:
        # Récupérer les données
        data = request.get_json()
        
        # Ajouter ID et date
        prediction_data = {
            "id": next_id,
            "date_prediction": datetime.now().isoformat(),
            **data
        }
        
        # Ajouter à l'historique
        predictions_history.append(prediction_data)
        next_id += 1
        
        return jsonify({"id": prediction_data["id"], "status": "success"})
        
    except Exception as e:
        error_msg = f"Erreur lors de la sauvegarde de la prédiction: {str(e)}"
        print(f"❌ {error_msg}")
        print(traceback.format_exc())
        return jsonify({"error": error_msg}), 500

@app.route('/mock-predictions', methods=['GET'])
def get_mock_predictions():
    """Endpoint pour servir des données de test avec les mêmes features que le modèle"""
    try:
        from datetime import datetime, timedelta
        
        # Données d'exemple pour les prédictions avec TOUTES les features
        mock_data = []
        for i in range(5):
            # Alterner entre accident grave et léger
            is_grave = i % 2 == 0
            
            mock_data.append({
                "id": i + 1,
                "date_prediction": (datetime.now() - timedelta(days=i)).isoformat(),
                # Features catégorielles
                "sexe": 1 if i % 2 == 0 else 2,  # 1=homme, 2=femme
                "catu": 1,                        # catégorie d'usager
                "trajet": i % 5,                  # motif du trajet
                "secu1": 1,                       # équipement de sécurité
                "agg": 1,                         # en agglomération
                "dep": 75 + i,                    # département
                # Features numériques
                "age": 30 + (i * 10),
                "place": 1,                       # place dans le véhicule
                "catv": 7,                        # catégorie de véhicule
                "atm": 1,                         # conditions atmosphériques
                "lum": 1,                         # luminosité
                "circ": 1,                        # régime de circulation
                "choc": 1,                        # point de choc
                "manv": 1,                        # manœuvre avant l'accident
                "motor": 1,                       # type de motorisation
                "vma": 50 + (i * 20),             # vitesse max autorisée
                # Résultat de la prédiction
                "prediction": 1 if is_grave else 0,
                "probability": 0.7 + (0.2 if is_grave else -0.2),
                "severity": "Grave" if is_grave else "Léger"
            })
            
        return jsonify(mock_data)
        
    except Exception as e:
        print(f"Erreur dans mock-predictions: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Exemple pour le backend Flask
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print(f"Données reçues pour prédiction: {data}")
        
        # Logique de prédiction simplifiée
        # Dans un cas réel, vous utiliseriez un modèle ML ici
        
        # Calcul d'une probabilité basée sur les facteurs de risque
        is_night = int(data.get('lum', 1)) >= 3  # Nuit si lum >= 3
        high_speed = int(data.get('vma', 50)) >= 90  # Vitesse élevée
        motorcycle = int(data.get('catv', 7)) in [30, 31, 32, 33, 34]  # Moto
        bad_weather = int(data.get('atm', 1)) >= 2  # Mauvais temps
        young_old = int(data.get('age', 30)) > 65 or int(data.get('age', 30)) < 25  # Jeune ou senior
        
        # Facteurs qui augmentent la probabilité d'accident grave
        probability = 0.5  # Probabilité de base
        if is_night: probability += 0.1
        if high_speed: probability += 0.25
        if motorcycle: probability += 0.15
        if bad_weather: probability += 0.1
        if young_old: probability += 0.1
        
        # S'assurer que la probabilité reste entre 0.1 et 0.9
        probability = min(0.9, max(0.1, probability))
        
        severity = "Grave" if probability > 0.5 else "Léger"
        
        # Sauvegarder la prédiction
        prediction_data = {
            **data,
            "severity": severity,
            "probability": probability,
            "prediction": 1 if probability > 0.5 else 0
        }
        
        save_prediction(prediction_data)
        
        return jsonify({
            'severity': severity,
            'probability': probability
        })
    except Exception as e:
        print(f"Erreur détaillée: {traceback.format_exc()}")
        app.logger.error(f"Erreur: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Fonction utilitaire pour la sauvegarde interne
def save_prediction(prediction_data):
    global next_id
    try:
        # Ajouter ID et date
        saved_data = {
            "id": next_id,
            "date_prediction": datetime.now().isoformat(),
            **prediction_data
        }
        
        # Ajouter à l'historique
        predictions_history.append(saved_data)
        next_id += 1
        
        return {"id": saved_data["id"], "status": "success"}
    except Exception as e:
        print(f"❌ Erreur interne lors de la sauvegarde: {str(e)}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Ajouter quelques données initiales
    for i in range(3):
        save_prediction({
            "sexe": 1 if i % 2 == 0 else 2,
            "age": 30 + i*10,
            "dep": 75,
            "catu": 1,
            "trajet": 0,
            "secu1": 1,
            "agg": 1,
            "place": 1,
            "catv": 7,
            "atm": 1,
            "lum": 1,
            "circ": 1,
            "choc": 1,
            "manv": 1,
            "motor": 1,
            "vma": 50 + i*20,
            "severity": "Grave" if i % 2 == 0 else "Léger",
            "probability": 0.8 - (i * 0.2),
            "prediction": 1 if i % 2 == 0 else 0
        })
    
    print("✅ Historique initialisé avec 3 exemples")
    app.run(debug=True)