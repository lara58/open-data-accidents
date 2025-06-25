
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