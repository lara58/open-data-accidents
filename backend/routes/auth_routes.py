from flask import Blueprint, request, jsonify
import jwt
import datetime
# Importer le décorateur token_required
from utils.auth_decorator import token_required

auth_bp = Blueprint("auth", __name__)

# Clé secrète pour JWT
SECRET_KEY = "votre_cle_secrete_a_changer"

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email et mot de passe requis"}), 400
    
    # Version simplifiée pour tester
    if data.get('email') == "admin@example.com" and data.get('password') == "password123":
        user_id = 1
        username = "admin"
    else:
        return jsonify({"error": "Email ou mot de passe incorrect"}), 401
    
    # Générer un token JWT
    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm="HS256")
    
    return jsonify({
        'token': token,
        'user_id': user_id,
        'username': username
    }), 200

# Modifier cette route pour ne pas utiliser token_required pour l'instant
@auth_bp.route("/user", methods=["GET"])
def get_user_info():
    """Version simplifiée sans authentification pour tests"""
    user_id = request.args.get('id', 1, type=int)
    
    # Données mockées pour tests
    user = {
        'id': user_id,
        'username': 'admin' if user_id == 1 else f'user{user_id}',
        'email': f'user{user_id}@example.com'
    }
    
    return jsonify(user), 200

# Route de test
@auth_bp.route("/test", methods=["GET"])
def test_auth():
    return jsonify({"message": "Auth API accessible"}), 200
