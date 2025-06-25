# Logique métier (filtrage, préparation data, etc...)


from models.accident_model import insert_accident, get_all_accidents, get_accident_by_id, get_all_accidents_for_user
from datetime import datetime


def enregistrer_accident(data, user_id):
    try:
        #validation date
        datetime.strptime(data["date_accident"], "%Y-%m-%d")
        insert_accident(data, user_id)
        return {"message": "Accident enregistré avec succès"}, 201
    except Exception as e:
        return {"error": f"Erreur d'enregistrement : {str(e)}"}, 400

def lister_accidents():
    try:
        data = get_all_accidents()
        return {"accidents": data}, 200
    except Exception as e:
        return {"error": str(e)}, 500
    
def lister_accidents_by_user(user_id):
    try:
        # Filtrer les accidents de l'utilisateur connecté uniquement
        data = get_all_accidents_for_user(user_id)
        return {"accidents": data}, 200
    except Exception as e:
        return {"error": str(e)}, 500


def lire_accident_par_id(accident_id):
    accident = get_accident_by_id(accident_id)
    if not accident:
        return {"error": "Accident introuvable"}, 404
    return accident, 200
