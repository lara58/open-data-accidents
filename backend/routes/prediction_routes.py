from flask import Blueprint, jsonify, request
from services.prediction_service import predict_from_data, predict_from_accident, list_predictions, list_user_predictions
import traceback

# Créer le blueprint pour les routes de prédiction
prediction_bp = Blueprint('predictions', __name__)

@prediction_bp.route('', methods=['GET'])
def get_predictions():
    """Retourne toutes les prédictions"""
    try:
        predictions = list_predictions()
        return jsonify(predictions)
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des prédictions: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@prediction_bp.route('', methods=['POST'])
def make_prediction():
    """Effectue une prédiction à partir des données POST"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Aucune donnée fournie"}), 400
            
        # Récupérer l'ID utilisateur du token JWT s'il existe
        user_id = None
        if 'Authorization' in request.headers:
            # Logique d'extraction de l'ID utilisateur du token JWT
            pass
            
        print(f"🔍 Données de prédiction reçues: {data}")
            
        # Effectuer la prédiction
        prediction = predict_from_data(data, user_id)
        
        if prediction:
            return jsonify(prediction), 201
        else:
            return jsonify({"error": "Impossible de réaliser la prédiction", 
                           "model_status": "non disponible"}), 500
            
    except Exception as e:
        print(f"❌ Erreur lors de la prédiction: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@prediction_bp.route('/from-accident/<int:accident_id>', methods=['POST'])
def predict_accident(accident_id):
    """Prédit à partir des données d'un accident existant"""
    try:
        # Récupérer l'ID utilisateur du token JWT s'il existe
        user_id = None
        if 'Authorization' in request.headers:
            # Logique d'extraction de l'ID utilisateur du token JWT
            pass
            
        prediction = predict_from_accident(accident_id, user_id)
        
        if prediction:
            return jsonify(prediction), 201
        else:
            return jsonify({"error": f"Impossible de prédire pour l'accident {accident_id}"}), 404
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@prediction_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_predictions(user_id):
    """Retourne les prédictions d'un utilisateur spécifique"""
    try:
        predictions = list_user_predictions(user_id)
        return jsonify(predictions)
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500