
import jwt
import datetime
from models.auth_model import insert_user, get_user_by_email
from werkzeug.security import generate_password_hash, check_password_hash


SECRET_KEY = "ta_clef_secrète"

def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def register_user(username, email, password):
    existing = get_user_by_email(email)
    if existing:
        return {"error": "Email déjà utilisé"}, 400
    hashed_password = generate_password_hash(password)
    try:
        user_id = insert_user(username, email, hashed_password)
        return {"message": "Inscription réussie", "user_id": user_id}, 201
    except Exception as e:
        # Gestion simple d'erreur (ex: utilisateur déjà existant)
        return {"error": str(e)}, 400


def login_user(email, password):
    user = get_user_by_email(email)
    if user and check_password_hash(user["password"], password):
        token = create_token(user["id"])
        return {"message": "Connexion réussie", "user": user["username"], "token": token}, 200
    else:
        return {"error": "Identifiants invalides"}, 401

