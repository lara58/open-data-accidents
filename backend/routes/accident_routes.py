# Routes API (GET / POST / FILTER / etc....)

from flask import Blueprint, request, jsonify
from models.accident_model import insert_accident, get_all_accidents, get_accident_by_id, update_accident, delete_accident
import traceback

accident_bp = Blueprint('accidents', __name__)

@accident_bp.route('/', methods=['GET'])
def get_accidents():
    try:
        accidents = get_all_accidents()
        return jsonify({"accidents": accidents})
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des accidents: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@accident_bp.route('/<int:accident_id>', methods=['GET'])
def get_accident(accident_id):
    try:
        accident = get_accident_by_id(accident_id)
        if accident:
            return jsonify(accident)
        else:
            return jsonify({"error": "Accident non trouvé"}), 404
    except Exception as e:
        print(f"❌ Erreur lors de la récupération de l'accident: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@accident_bp.route('/', methods=['POST'])
def create_accident():
    try:
        data = request.get_json()
        
        # Récupérer l'ID utilisateur (généralement extrait d'un token JWT)
        user_id = 1  # Utilisateur par défaut pour la démo
        
        # Si des données de mois/jour ne sont pas fournies, utiliser la date actuelle
        if 'mois' not in data or 'jour' not in data:
            from datetime import datetime
            now = datetime.now()
            data['mois'] = now.month
            data['jour'] = now.day
            
        accident_id = insert_accident(data, user_id)
        
        return jsonify({
            "message": "Accident enregistré avec succès",
            "accident_id": accident_id
        }), 201
        
    except Exception as e:
        print(f"❌ Erreur lors de la création d'un accident: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@accident_bp.route('/<int:accident_id>', methods=['PUT'])
def update_accident_route(accident_id):
    try:
        data = request.get_json()
        update_accident(accident_id, data)
        return jsonify({"message": f"Accident {accident_id} mis à jour avec succès"})
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour de l'accident: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@accident_bp.route('/<int:accident_id>', methods=['DELETE'])
def delete_accident_route(accident_id):
    try:
        delete_accident(accident_id)
        return jsonify({"message": f"Accident {accident_id} supprimé avec succès"})
    except Exception as e:
        print(f"❌ Erreur lors de la suppression de l'accident: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

