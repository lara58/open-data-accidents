import os
import duckdb  # Remplacer sqlite3 par duckdb
import sys

# Obtenir le chemin absolu vers le répertoire racine du projet
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

def get_db_connection():
    """Établit et renvoie une connexion à la base de données DuckDB."""
    db_path = os.path.join(PROJECT_ROOT, 'backend', 'accidents.db')
    # DuckDB utilise une syntaxe légèrement différente pour la connexion
    conn = duckdb.connect(db_path)
    # Note: DuckDB n'a pas besoin de row_factory comme SQLite
    return conn

def init_db():
    conn = get_db_connection()
    sql_file_path = os.path.join(os.path.dirname(__file__), 'init_db.sql')
    
    print(f"Initialisation de la base de données DuckDB avec le fichier: {sql_file_path}")
    
    # Lire et exécuter le script SQL
    with open(sql_file_path, 'r') as f:
        sql_script = f.read()
        # DuckDB peut exécuter plusieurs instructions SQL à la fois
        conn.execute(sql_script)
    
    # Fermer la connexion (DuckDB effectue un commit automatique à la fermeture)
    conn.close()
    print("Base de données DuckDB initialisée avec succès.")

if __name__ == "__main__":
    init_db()