# Fichier SQL pour init la base

# backend/connection.py

import duckdb
import os

# Connexion à une base persistante
db_path = os.path.join(os.path.dirname(__file__), '../../accidents.duckdb')

def get_db_connection():
    return duckdb.connect(database=db_path, read_only=False)
   
