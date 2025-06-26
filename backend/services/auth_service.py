import os
import jwt
from datetime import datetime, timedelta
from models.auth_model import get_user_by_email, insert_user, get_user_by_id

# Clé secrète pour JWT (utiliser variable d'environnement en production)
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'ta_cle_secrete_a_changer_en_production')

def register_user(user_data):
    """
    Enregistre un nouvel utilisateur
    """
    # Vérifier si l'email existe déjà
    existing_user = get_user_by_email(user_data.get('email'))
    if existing_user:
        return None, "Cet email est déjà utilisé"
    
    # Hasher le mot de passe (en production, utiliser bcrypt)
    # password_hash = generate_password_hash(user_data.get('password'))
    
    # Enregistrer l'utilisateur
    user_id = insert_user({
        'username': user_data.get('username'),
        'email': user_data.get('email'),
        'password': user_data.get('password')  # En production, utiliser password_hash
    })
    
    return user_id, None

def login_user(email, password):
    """
    Authentifie un utilisateur et retourne ses données
    """
    # Récupérer l'utilisateur par email
    user = get_user_by_email(email)
    
    # Vérifier si l'utilisateur existe
    if not user:
        return None, "Email ou mot de passe incorrect"
    
    # Vérifier le mot de passe (en production, utiliser check_password_hash)
    if user.get('password') != password:
        return None, "Email ou mot de passe incorrect"
    
    return user, None

def generate_token(user_id):
    """
    Génère un token JWT pour un utilisateur donné
    """
    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, SECRET_KEY, algorithm="HS256")
    
    return token

def verify_token(token):
    """
    Vérifie un token JWT et retourne les données décodées
    """
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return data
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None