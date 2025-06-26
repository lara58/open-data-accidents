from db.connection import get_db_connection


def verify_user(email, password):
    """
    Vérifie les identifiants utilisateur et retourne les infos utilisateur si valides.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?',
                   (email, password))

    user = cursor.fetchone()
    conn.close()
    
    # Conversion spécifique pour DuckDB
    if user:
        column_names = [desc[0] for desc in cursor.description]
        return {column_names[i]: value for i, value in enumerate(user)}
    return None


def get_user_by_id(user_id):
    """
    Récupère les informations d'un utilisateur par son ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    # Conversion spécifique pour DuckDB
    if user:
        column_names = [desc[0] for desc in cursor.description]
        return {column_names[i]: value for i, value in enumerate(user)}
    return None


def get_user_by_email(email):
    """
    Récupère les informations d'un utilisateur par son email
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    
    # Conversion spécifique pour DuckDB
    if user:
        column_names = [desc[0] for desc in cursor.description]
        return {column_names[i]: value for i, value in enumerate(user)}
    return None


def insert_user(user_data):
    """
    Insère un nouvel utilisateur dans la base de données
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Récupérer le max id existant pour l'auto-incrémentation manuelle
    cursor.execute("SELECT MAX(id) FROM users")
    max_id = cursor.fetchone()[0] or 0
    next_id = max_id + 1

    cursor.execute(
        'INSERT INTO users (id, username, email, password) VALUES (?, ?, ?, ?)',
        (next_id, user_data.get('username'), user_data.get('email'), user_data.get('password'))
    )

    conn.commit()
    conn.close()

    return next_id

