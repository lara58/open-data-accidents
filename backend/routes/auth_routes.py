

from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user
from utils.auth_decorator import token_required

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