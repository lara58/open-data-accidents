# Requêtes SQL/ORM liées aux accidents

from db.connection import get_db_connection

def get_all_accidents():
    conn = get_db_connection()
    return conn.execute("SELECT * FROM accidents").fetchall()

def get_accidents_by_year(year):
    conn = get_db_connection()
    return conn.execute("SELECT * FROM accidents WHERE year = ?", (year,)).fetchall()
