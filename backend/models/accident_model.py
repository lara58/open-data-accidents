# Requêtes SQL/ORM liées aux accidents

from db.connection import get_db_connection
from services.predictor import predire_gravite  # Cette fonction doit renvoyer 0 ou 1



# def insert_accident(data, user_id):
#     conn = get_db_connection()

#     required_numeric_fields = [
#         "lieu_departement", "agglomeration", "type_route", "condition_meteo", "luminosite",
#         "categorie_vehicule", "categorie_usager", "age", "motif_deplacement", "equipement_securite",
#         "place_usager", "sexe_usager", "manoeuvre_principal_accident", "type_moteur",
#         "vitesse_max", "point_choc_initial"
#     ]

#     for field in required_numeric_fields:
#         if field not in data:
#             raise ValueError(f"Le champ requis '{field}' est manquant.")
#         if not isinstance(data[field], int):
#             raise TypeError(f"Le champ '{field}' doit être un entier (INTEGER).")

#     # Récupérer le max id
#     result = conn.execute("SELECT MAX(id) FROM accidents").fetchone()
#     new_id = (result[0] or 0) + 1

#     conn.execute("""
#         INSERT INTO accidents (
#             id, user_id, date_accident, heure_accident, lieu_code_insee, lieu_departement, lieu_commune,
#             lieu_latitude, lieu_longitude, agglomeration, type_route, condition_meteo,
#             luminosite, collision_type, gravite_accident, nb_vehicules, categorie_vehicule,
#             nb_usagers, categorie_usager, age, motif_deplacement, equipement_securite,
#             place_usager, sexe_usager, manoeuvre_principal_accident, type_moteur,
#             vitesse_max, point_choc_initial, description
#         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, (
#         new_id, user_id, data["date_accident"], data.get("heure_accident"),
#         data.get("lieu_code_insee"), data["lieu_departement"], data.get("lieu_commune"),
#         data.get("lieu_latitude"), data.get("lieu_longitude"), data["agglomeration"],
#         data["type_route"], data["condition_meteo"], data["luminosite"],
#         data.get("collision_type"), data.get("gravite_accident"), data.get("nb_vehicules"),
#         data["categorie_vehicule"], data.get("nb_usagers"), data["categorie_usager"],
#         data["age"], data["motif_deplacement"], data["equipement_securite"],
#         data["place_usager"], data["sexe_usager"], data["manoeuvre_principal_accident"],
#         data["type_moteur"], data["vitesse_max"], data["point_choc_initial"],
#         data.get("description")
#     ))

#     conn.commit()
#     return new_id


def insert_accident(data, user_id):
    conn = get_db_connection()

    required_numeric_fields = [
        "lieu_departement", "agglomeration", "type_route", "condition_meteo", "luminosite",
        "categorie_vehicule", "categorie_usager", "age", "motif_deplacement", "equipement_securite",
        "place_usager", "sexe_usager", "manoeuvre_principal_accident", "type_moteur",
        "vitesse_max", "point_choc_initial"
    ]

    # Vérification des champs obligatoires
    for field in required_numeric_fields:
        if field not in data:
            raise ValueError(f"Le champ requis '{field}' est manquant.")
        if not isinstance(data[field], int):
            raise TypeError(f"Le champ '{field}' doit être un entier (INTEGER).")

    # Prédiction automatique de la gravité (0 ou 1)
    gravite_predite = str(predire_gravite(data))

    # Générer un nouvel ID
    result = conn.execute("SELECT MAX(id) FROM accidents").fetchone()
    new_id = (result[0] or 0) + 1

    # Insertion des données
    conn.execute("""
        INSERT INTO accidents (
            id, user_id, date_accident, heure_accident, lieu_code_insee, lieu_departement, lieu_commune,
            lieu_latitude, lieu_longitude, agglomeration, type_route, condition_meteo,
            luminosite, collision_type, gravite_accident, nb_vehicules, categorie_vehicule,
            nb_usagers, categorie_usager, age, motif_deplacement, equipement_securite,
            place_usager, sexe_usager, manoeuvre_principal_accident, type_moteur,
            vitesse_max, point_choc_initial, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        new_id, user_id, data["date_accident"], data.get("heure_accident"),
        data.get("lieu_code_insee"), data["lieu_departement"], data.get("lieu_commune"),
        data.get("lieu_latitude"), data.get("lieu_longitude"), data["agglomeration"],
        data["type_route"], data["condition_meteo"], data["luminosite"],
        data.get("collision_type"), gravite_predite, data.get("nb_vehicules"),
        data["categorie_vehicule"], data.get("nb_usagers"), data["categorie_usager"],
        data["age"], data["motif_deplacement"], data["equipement_securite"],
        data["place_usager"], data["sexe_usager"], data["manoeuvre_principal_accident"],
        data["type_moteur"], data["vitesse_max"], data["point_choc_initial"],
        data.get("description")
    ))

    conn.commit()
    return new_id



def get_all_accidents():
    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM accidents")
    rows = cursor.fetchall()
    keys = [col[0] for col in cursor.description]
    return [dict(zip(keys, row)) for row in rows]

def get_accident_by_id(accident_id):
    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM accidents WHERE id = ?", (accident_id,))
    row = cursor.fetchone()
    if not row:
        return None
    keys = [col[0] for col in cursor.description]
    return dict(zip(keys, row))

def get_all_accidents_for_user(user_id):
    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM accidents WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    keys = [col[0] for col in cursor.description]
    return [dict(zip(keys, row)) for row in rows]

def update_accident(accident_id, data):
    conn = get_db_connection()
    columns = ", ".join(f"{key} = ?" for key in data.keys())
    values = list(data.values()) + [accident_id]
    conn.execute(f"UPDATE accidents SET {columns} WHERE id = ?", values)
    conn.commit()

def delete_accident(accident_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM accidents WHERE id = ?", (accident_id,))
    conn.commit()
