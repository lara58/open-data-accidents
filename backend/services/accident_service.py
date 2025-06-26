from flask import jsonify
import traceback
from models.accident_model import insert_accident, get_all_accidents, get_accident_by_id, get_all_accidents_for_user, update_accident, delete_accident

def enregistrer_accident(data, user_id):
    """
    Enregistre un nouvel accident dans la base de données
    """
    try:
        # Ajout de l'utilisateur aux données
        data["user_id"] = user_id
        
        # Appel à la fonction du modèle pour l'insertion
        accident_id = insert_accident(data, user_id)
        
        return jsonify({
            "message": "Accident enregistré avec succès",
            "accident_id": accident_id
        }), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

def lister_accidents():
    """
    Récupère tous les accidents de la base de données
    """
    try:
        accidents = get_all_accidents()
        return jsonify(accidents), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

def lire_accident_par_id(accident_id):
    """
    Récupère les détails d'un accident spécifique
    """
    try:
        accident = get_accident_by_id(accident_id)
        
        if not accident:
            return jsonify({"error": "Accident introuvable"}), 404
            
        return jsonify(accident), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

def lister_accidents_by_user(user_id):
    """
    Récupère tous les accidents créés par un utilisateur spécifique
    """
    try:
        accidents = get_all_accidents_for_user(user_id)
        return jsonify(accidents), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

def modifier_accident(accident_id, data, user_id):
    """
    Modifie un accident existant
    L'utilisateur ne peut modifier que ses propres accidents
    """
    try:
        accident = get_accident_by_id(accident_id)
        
        if not accident:
            return jsonify({"error": "Accident introuvable"}), 404
            
        # Vérifier que l'accident appartient à l'utilisateur
        if accident["user_id"] != user_id:
            return jsonify({"error": "Non autorisé - Vous ne pouvez modifier que vos propres accidents"}), 403
            
        update_accident(accident_id, data)
        return jsonify({"message": "Accident modifié avec succès"}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

def supprimer_accident(accident_id, user_id):
    """
    Supprime un accident existant
    L'utilisateur ne peut supprimer que ses propres accidents
    """
    try:
        accident = get_accident_by_id(accident_id)
        
        if not accident:
            return jsonify({"error": "Accident introuvable"}), 404
            
        # Vérifier que l'accident appartient à l'utilisateur
        if accident["user_id"] != user_id:
            return jsonify({"error": "Non autorisé - Vous ne pouvez supprimer que vos propres accidents"}), 403
            
        delete_accident(accident_id)
        return jsonify({"message": "Accident supprimé avec succès"}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500