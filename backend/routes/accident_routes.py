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