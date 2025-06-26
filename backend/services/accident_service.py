# Logique métier (filtrage, préparation data, etc...)


from models.accident_model import insert_accident, get_all_accidents, get_accident_by_id, get_all_accidents_for_user
from services.train_modele import predire_gravite
from datetime import datetime

# def enregistrer_accident(data, user_id):
#     try:
#         datetime.strptime(data["date_accident"], "%Y-%m-%d")  # Vérifie format de la date
#         insert_accident(data, user_id)
#         return {"message": "Accident enregistré avec succès"}, 201
#     except (ValueError, TypeError) as e:
#         return {"error": f"Erreur de validation : {str(e)}"}, 400
#     except Exception as e:
#         return {"error": f"Erreur interne : {str(e)}"}, 500



REQUIRED_NUMERIC_FIELDS = [
    "lieu_departement", "agglomeration", "type_route", "condition_meteo", "luminosite",
    "categorie_vehicule", "categorie_usager", "age", "motif_deplacement", "equipement_securite",
    "place_usager", "sexe_usager", "manoeuvre_principal_accident", "type_moteur",
    "vitesse_max", "point_choc_initial"
]


def enregistrer_accident(data, user_id):
    try:
        # Vérification du format de la date
        datetime.strptime(data["date_accident"], "%Y-%m-%d")

        # Validation des champs obligatoires
        for field in REQUIRED_NUMERIC_FIELDS:
            if field not in data:
                raise ValueError(f"Champ obligatoire manquant : {field}")
            if not isinstance(data[field], int):
                raise TypeError(f"Le champ '{field}' doit être un entier.")

        # Supprimer toute tentative d'ajout manuel de la gravité
        if "gravite_accident" in data:
            del data["gravite_accident"]

        # Prédiction automatique de la gravité et le score
        gravite, pourcentage = predire_gravite(data)
        
        data["gravite_accident"] = gravite
        data["gravite_accident_proba"] = f"{pourcentage:.2f}%"  # Exemple : "87.50%"

        # Enregistrement dans la base
        insert_accident(data, user_id)

        return {"message": "Accident enregistré avec gravité prédite."}, 201

    except (ValueError, TypeError) as e:
        return {"error": f"Erreur de validation : {str(e)}"}, 400
    except Exception as e:
        return {"error": f"Erreur interne : {str(e)}"}, 500


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
