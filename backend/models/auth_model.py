
from db.connection import get_db_connection


def insert_user(username, email, hashed_password):
    conn = get_db_connection()

    # Récupérer le max id existant
    result = conn.execute("SELECT MAX(id) FROM users").fetchone()
    print(result)
    max_id = result[0] if result[0] is not None else 0
    new_id = max_id + 1

    # Insérer le nouvel utilisateur avec l'id calculé
    conn.execute(
        "INSERT INTO users (id, username, email, password) VALUES (?, ?, ?, ?);",
        (new_id, username, email, hashed_password)
    )
    conn.commit()
    return new_id

def get_user_by_email(email):
    conn = get_db_connection()
    result = conn.execute("SELECT * FROM users WHERE email = ?;", (email,)).fetchone()
    if result is None:
        return None
    # Conversion en dict avec noms de colonnes
    keys = ["id", "username", "email", "password"]
    return dict(zip(keys, result))


def get_user_by_id(user_id):
    conn = get_db_connection()
    result = conn.execute("SELECT * FROM users WHERE id = ?;", (user_id,)).fetchone()
    if result is None:
        return None
    keys = ["id", "username", "email", "password"]
    return dict(zip(keys, result))


def update_user_profile(user_id, username, email):
    conn = get_db_connection()

    # Vérifie si l'email est utilisé par un autre utilisateur
    result = conn.execute("SELECT id FROM users WHERE email = ?;", (email,)).fetchone()
    if result and result[0] != user_id:
        raise ValueError("Email déjà utilisé par un autre utilisateur")

    try:
        conn.execute(
            "UPDATE users SET username = ?, email = ? WHERE id = ?;",
            (username, email, user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print("Erreur update_user_profile:", e)
        return False



def update_user_password(user_id, hashed_password):
    conn = get_db_connection()
    conn.execute(
        "UPDATE users SET password = ? WHERE id = ?;",
        (hashed_password, user_id)
    )
    conn.commit()
    return True

