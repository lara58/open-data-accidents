# Routes API (GET / POST / FILTER / etc....)

from flask import Blueprint, request, jsonify
from services.accident_service import enregistrer_accident, lister_accidents, lire_accident_par_id, lister_accidents_by_user
from utils.auth_decorator import token_required

accident_bp = Blueprint("accidents", __name__)

@accident_bp.route("", methods=["POST"])
@token_required
def ajouter(user_id):
    data = request.get_json()
    return enregistrer_accident(data, user_id)


@accident_bp.route("", methods=["GET"])
@token_required
def lire_tous(user_id):
    return lister_accidents()


@accident_bp.route("/user", methods=["GET"])
@token_required
def lire_perso(user_id):
    return lister_accidents_by_user(user_id)


@accident_bp.route("/<int:accident_id>", methods=["GET"])
@token_required
def lire_un(user_id, accident_id):
    return lire_accident_par_id(accident_id)

@accident_bp.route("/<int:accident_id>", methods=["PUT"])
@token_required
def modifier(user_id, accident_id):
    from models.accident_model import get_accident_by_id, update_accident
    accident = get_accident_by_id(accident_id)
    if not accident:
        return jsonify({"error": "Accident introuvable"}), 404
    if accident["user_id"] != user_id:
        return jsonify({"error": "Non autorisé"}), 403

    data = request.get_json()
    update_accident(accident_id, data)
    return jsonify({"message": "Accident modifié"}), 200


@accident_bp.route("/<int:accident_id>", methods=["DELETE"])
@token_required
def supprimer(user_id, accident_id):
    from models.accident_model import get_accident_by_id, delete_accident
    accident = get_accident_by_id(accident_id)
    if not accident:
        return jsonify({"error": "Accident introuvable"}), 404
    if accident["user_id"] != user_id:
        return jsonify({"error": "Non autorisé"}), 403

    delete_accident(accident_id)
    return jsonify({"message": "Accident supprimé"}), 200

