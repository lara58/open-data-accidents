import os
import duckdb

# Chemin vers le répertoire racine du projet
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_db_connection():
    """Établit et renvoie une connexion à la base de données DuckDB."""
    db_path = os.path.join(PROJECT_ROOT, 'accidents.db')
    conn = duckdb.connect(db_path)
    return conn