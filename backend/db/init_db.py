# Configuration Flask + BDD

import os
from backend.db.connection import get_db_connection

def init_db():
    conn = get_db_connection()
    sql_file_path = os.path.join(os.path.dirname(__file__), 'init_db.sql')  # chemin absolu vers init_db.sql
    with open(sql_file_path, 'r') as f:
        conn.execute(f.read())
    print("Base de données initialisée.")

if __name__ == "__main__":
    init_db()
