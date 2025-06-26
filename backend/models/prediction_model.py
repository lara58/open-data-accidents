from db.connection import get_db_connection
from datetime import datetime

def save_prediction(prediction_data):
    """
    Enregistre une prédiction dans la base de données
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Vérifier si le système d'auto-incrémentation fonctionne
        cursor.execute("SELECT MAX(id) FROM predictions")
        max_id = cursor.fetchone()[0]
        next_id = 1 if max_id is None else max_id + 1
        
        # Définir les champs à insérer, en ajoutant explicitement l'ID
        prediction_data['id'] = next_id
        
        # Construire la requête d'insertion de manière dynamique
        columns = ', '.join(prediction_data.keys())
        placeholders = ', '.join(['?' for _ in prediction_data])
        values = list(prediction_data.values())
        
        # Exécuter la requête
        query = f"INSERT INTO predictions ({columns}) VALUES ({placeholders})"
        cursor.execute(query, values)
        
        # DuckDB commit automatique à la fermeture de connexion
        conn.close()
        
        return next_id
    except Exception as e:
        print(f"❌ Erreur lors de l'enregistrement de la prédiction: {e}")
        conn.close()
        return None

def get_predictions():
    """
    Récupère toutes les prédictions de la base de données
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Exécuter la requête
        cursor.execute("SELECT * FROM predictions")
        rows = cursor.fetchall()
        
        # Obtenir les noms des colonnes
        columns = [col[0] for col in cursor.description]
        
        # Convertir les résultats en liste de dictionnaires
        predictions = []
        for row in rows:
            prediction = {}
            for i, value in enumerate(row):
                prediction[columns[i]] = value
            predictions.append(prediction)
        
        return predictions
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des prédictions: {e}")
        return []
    finally:
        conn.close()

def get_predictions_by_user(user_id):
    """
    Récupère les prédictions d'un utilisateur spécifique
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Exécuter la requête
        cursor.execute("SELECT * FROM predictions WHERE user_id = ?", [user_id])
        rows = cursor.fetchall()
        
        # Obtenir les noms des colonnes
        columns = [col[0] for col in cursor.description]
        
        # Convertir les résultats en liste de dictionnaires
        predictions = []
        for row in rows:
            prediction = {}
            for i, value in enumerate(row):
                prediction[columns[i]] = value
            predictions.append(prediction)
        
        return predictions
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des prédictions de l'utilisateur: {e}")
        return []
    finally:
        conn.close()

def get_prediction_detail(prediction_id):
    """
    Récupère les détails d'une prédiction spécifique
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Exécuter la requête
        cursor.execute("SELECT * FROM predictions WHERE id = ?", [prediction_id])
        row = cursor.fetchone()
        
        if not row:
            return None
            
        # Obtenir les noms des colonnes
        columns = [col[0] for col in cursor.description]
        
        # Convertir le résultat en dictionnaire
        prediction = {}
        for i, value in enumerate(row):
            prediction[columns[i]] = value
        
        return prediction
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des détails de la prédiction: {e}")
        return None
    finally:
        conn.close()

def remove_prediction(prediction_id):
    """
    Supprime une prédiction de la base de données
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Vérifier si la prédiction existe
        cursor.execute("SELECT id FROM predictions WHERE id = ?", [prediction_id])
        if not cursor.fetchone():
            return False
            
        # Exécuter la requête de suppression
        cursor.execute("DELETE FROM predictions WHERE id = ?", [prediction_id])
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la suppression de la prédiction: {e}")
        return False
    finally:
        conn.close()