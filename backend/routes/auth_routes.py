

from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user
from utils.auth_decorator import token_required
from werkzeug.security import generate_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    response, status_code = register_user(username, email, password)
    return jsonify(response), status_code


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email et mot de passe sont requis"}), 400
    
    
    response, status_code = login_user(email, password)
    return jsonify(response), status_code


@auth_bp.route("/profile", methods=["GET"])
@token_required
def profile(user_id):
    from models.auth_model import get_user_by_id
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404
    return jsonify({"id": user["id"], "username": user["username"], "email": user["email"]}), 200


@auth_bp.route("/update-profile", methods=["PUT"])
@token_required
def update_profile(user_id):
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    
    if not username or not email:
        return jsonify({"error": "Champs requis"}), 400

    from models.auth_model import update_user_profile
    success = update_user_profile(user_id, username, email)
    if success:
        return jsonify({"message": "Profil mis à jour"}), 200
    return jsonify({"error": "Erreur lors de la mise à jour"}), 500


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    email = data.get("email")
    new_password = data.get("new_password")
    
    from models.auth_model import get_user_by_email, update_user_password
    user = get_user_by_email(email)
    if not user:
        return jsonify({"error": "Email inconnu"}), 404

    hashed_pw = generate_password_hash(new_password)
    update_user_password(user["id"], hashed_pw)
    return jsonify({"message": "Mot de passe mis à jour"}), 200
