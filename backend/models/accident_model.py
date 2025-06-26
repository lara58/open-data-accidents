# Requêtes SQL/ORM liées aux accidents

from db.connection import get_db_connection

def insert_accident(data, user_id):
    conn = get_db_connection()

    # Récupérer le max id existant dans la table accidents
    result = conn.execute("SELECT MAX(id) FROM accidents").fetchone()
    max_id = result[0] if result[0] is not None else 0
    new_id = max_id + 1

    conn.execute("""
        INSERT INTO accidents (
            id, user_id, mois, jour, lieu_code_insee, lieu_departement, lieu_commune,
            lieu_latitude, lieu_longitude, agglomeration, type_route, condition_meteo,
            luminosite, collision_type, gravite_accident, nb_vehicules, categorie_vehicule,
            nb_usagers, categorie_usager, age, motif_deplacement, equipement_securite,
            place_usager, sexe_usager, manoeuvre_principal_accident, type_moteur,
            vitesse_max, point_choc_initial, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        new_id,
        user_id,
        data.get("mois", 1),  # Valeur par défaut = 1
        data.get("jour", 1),   # Valeur par défaut = 1
        data.get("lieu_code_insee"),
        data.get("lieu_departement"),
        data.get("lieu_commune"),
        data.get("lieu_latitude"),
        data.get("lieu_longitude"),
        data.get("agglomeration"),
        data.get("type_route"),
        data.get("condition_meteo"),
        data.get("luminosite"),
        data.get("collision_type"),
        data.get("gravite_accident"),
        data.get("nb_vehicules"),
        data.get("categorie_vehicule"),
        data.get("nb_usagers"),
        data.get("categorie_usager"),
        data.get("age"),
        data.get("motif_deplacement"),
        data.get("equipement_securite"),
        data.get("place_usager"),
        data.get("sexe_usager"),
        data.get("manoeuvre_principal_accident"),
        data.get("type_moteur"),
        data.get("vitesse_max"),
        data.get("point_choc_initial"),
        data.get("description"),
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
