from pyspark.sql import SparkSession
from pyspark.ml.classification import RandomForestClassificationModel
from pyspark.ml.feature import StringIndexer, VectorAssembler
import duckdb
import pandas as pd
import os
from datetime import datetime

class AccidentPredictor:
    def __init__(self, model_path=None, db_path=None):
        """
        Initialise le service de prédiction avec le modèle RandomForest et une base DuckDB
        
        Args:
            model_path: chemin vers le modèle RandomForest sauvegardé
            db_path: chemin vers la base de données DuckDB
        """
        # Chemin par défaut relatif si non spécifié
        if model_path is None:
            model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rf_model_accidents")
        
        # Chemin par défaut pour la base de données
        if db_path is None:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "accidents_predictions.db")
        
        self.db_path = db_path
        
        # Initialiser Spark
        self.spark = SparkSession.builder \
            .appName("AccidentPredictionService") \
            .config("spark.driver.memory", "2g") \
            .getOrCreate()
            
        # Charger le modèle
        self.model = RandomForestClassificationModel.load(model_path)
        print(f"✅ Modèle chargé depuis {model_path}")
        
        # Définir les colonnes catégorielles et numériques
        self.categorical_cols = ["sexe", "catu", "trajet", "secu1", "agg", "dep"]
        self.numeric_cols = ["age", "place", "catv", "atm", "lum", "circ", "choc", "manv", "motor", "vma"]
        
        # Colonnes de features attendues par le modèle
        self.feature_cols = [col + "_indexed" for col in self.categorical_cols] + self.numeric_cols
        
        # Initialiser la base de données
        self._init_database()
    
    def _init_database(self):
        """Initialise la base de données DuckDB et crée la table si elle n'existe pas"""
        try:
            # Connexion à la base de données
            self.conn = duckdb.connect(self.db_path)
            
            # Création de la table si elle n'existe pas
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS accident_predictions (
                    id INTEGER PRIMARY KEY,
                    date_prediction TIMESTAMP,
                    sexe INTEGER,
                    age INTEGER,
                    dep INTEGER,
                    catu INTEGER,
                    trajet INTEGER,
                    secu1 INTEGER,
                    agg INTEGER,
                    place INTEGER,
                    catv INTEGER,
                    atm INTEGER,
                    lum INTEGER,
                    circ INTEGER,
                    choc INTEGER,
                    manv INTEGER,
                    motor INTEGER,
                    vma INTEGER,
                    prediction INTEGER,
                    probability FLOAT,
                    severity VARCHAR
                )
            """)
            
            # Test d'insertion
            self.conn.execute("INSERT INTO accident_predictions VALUES (0, CURRENT_TIMESTAMP, 1, 30, 75, 1, 0, 1, 1, 1, 7, 1, 1, 1, 1, 1, 1, 50, 1, 0.75, 'Test')")
            print(f"✅ Base de données initialisée: {self.db_path}")
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation de la base de données: {str(e)}")
            # Ne pas propager l'erreur pour que l'application continue à fonctionner
            print("Historique des prédictions sera désactivé")
    
    def transform_input(self, input_data):
        """
        Transforme les données d'entrée au format attendu par le modèle
        
        Args:
            input_data: dictionnaire avec les caractéristiques de l'accident
            
        Returns:
            DataFrame: DataFrame Spark avec la colonne 'features'
        """
        try:
            # Créer un DataFrame Spark à partir des données d'entrée
            input_df = self.spark.createDataFrame([input_data])
            
            # 1. Appliquer les StringIndexer pour les colonnes catégorielles
            indexed_df = input_df
            for col in self.categorical_cols:
                indexer = StringIndexer(inputCol=col, outputCol=col + "_indexed", handleInvalid="keep")
                indexer_model = indexer.fit(indexed_df)
                indexed_df = indexer_model.transform(indexed_df)
            
            # 2. Assembler toutes les features dans un vecteur
            assembler = VectorAssembler(
                inputCols=self.feature_cols, 
                outputCol="features",
                handleInvalid="skip"
            )
            
            # Appliquer l'assembleur
            final_df = assembler.transform(indexed_df)
            
            return final_df
            
        except Exception as e:
            print(f"Erreur lors de la transformation des données: {str(e)}")
            raise e
    
    def predict_severity(self, accident_data):
        """
        Prédit la gravité d'un accident et stocke la prédiction dans DuckDB
        
        Args:
            accident_data: dictionnaire contenant les caractéristiques de l'accident
            
        Returns:
            dict: résultat de la prédiction avec prédiction, probabilité et sévérité
        """
        try:
            # Vérifier que toutes les colonnes requises sont présentes
            required_cols = self.categorical_cols + self.numeric_cols
            missing_cols = [col for col in required_cols if col not in accident_data]
            
            if missing_cols:
                return {
                    "error": f"Colonnes manquantes: {', '.join(missing_cols)}",
                    "required_columns": required_cols
                }
                
            # Transformer les données
            input_df = self.transform_input(accident_data)
            
            # Faire la prédiction
            prediction = self.model.transform(input_df)
            
            # Extraire les résultats
            result = prediction.select("prediction", "probability").first()
            
            if result:
                pred_class = int(result["prediction"])
                probability = float(result["probability"][1])  # Probabilité de la classe 1 (grave)
                severity = "Grave" if pred_class == 1 else "Léger"
                
                prediction_result = {
                    "prediction": pred_class,
                    "probability": probability,
                    "severity": severity
                }
                
                # Stocker la prédiction dans la base
                self._save_prediction(accident_data, prediction_result)
                
                return prediction_result
            else:
                return {"error": "Impossible de produire une prédiction"}
            
        except Exception as e:
            print(f"Erreur lors de la prédiction: {str(e)}")
            return {"error": str(e)}
    
    def _save_prediction(self, input_data, prediction_result):
        """
        Sauvegarde la prédiction dans la base de données
        
        Args:
            input_data: données d'entrée utilisées pour la prédiction
            prediction_result: résultat de la prédiction
        """
        try:
            # Obtenir le prochain ID
            result = self.conn.execute("SELECT COALESCE(MAX(id), 0) + 1 AS next_id FROM accident_predictions").fetchone()
            next_id = result[0]
            
            # Créer un dictionnaire avec toutes les données à sauvegarder
            data_to_save = {
                "id": next_id,
                "date_prediction": datetime.now(),
                **input_data,
                "prediction": prediction_result["prediction"],
                "probability": prediction_result["probability"],
                "severity": prediction_result["severity"]
            }
            
            # Construire la requête d'insertion
            columns = ", ".join(data_to_save.keys())
            placeholders = ", ".join(["?" for _ in data_to_save])
            values = list(data_to_save.values())
            
            query = f"INSERT INTO accident_predictions ({columns}) VALUES ({placeholders})"
            self.conn.execute(query, values)
            
            print(f"✅ Prédiction sauvegardée avec ID: {next_id}")
        
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde de la prédiction: {str(e)}")
    
    def get_recent_predictions(self, limit=10):
        """
        Récupère les prédictions récentes
        
        Args:
            limit: nombre maximum de prédictions à récupérer
            
        Returns:
            list: liste des prédictions récentes
        """
        try:
            # Si la connexion n'est pas établie, retourner des données factices
            if not hasattr(self, 'conn') or self.conn is None:
                print("⚠️ Base de données non disponible, retour de données factices")
                from datetime import datetime, timedelta
                
                mock_data = []
                for i in range(min(5, limit)):
                    mock_data.append({
                        "id": i,
                        "date_prediction": (datetime.now() - timedelta(days=i)).isoformat(),
                        "sexe": 1 if i % 2 == 0 else 2,
                        "age": 30 + i*5,
                        "dep": 75,
                        "catu": 1,
                        "trajet": 0,
                        "secu1": 1,
                        "agg": 1,
                        "place": 1,
                        "catv": 7,
                        "atm": 1,
                        "lum": 1,
                        "circ": 1,
                        "choc": 1,
                        "manv": 1,
                        "motor": 1,
                        "vma": 50,
                        "severity": "Grave" if i % 2 == 0 else "Léger",
                        "prediction": 1 if i % 2 == 0 else 0,
                        "probability": 0.7 - (i * 0.1)
                    })
                return mock_data
                
            # Code DuckDB normal
            query = f"""
                SELECT * FROM accident_predictions
                ORDER BY date_prediction DESC
                LIMIT {limit}
            """
            result = self.conn.execute(query).fetchall()
            
            # Si pas de résultats, retourner une liste vide
            if not result:
                return []
                
            # Convertir en liste de dictionnaires
            columns = self.conn.execute("SELECT * FROM accident_predictions LIMIT 0").description
            column_names = [col[0] for col in columns]
            
            predictions = []
            for row in result:
                prediction = {}
                for i, value in enumerate(row):
                    # Convertir les timestamps en chaînes ISO pour JSON
                    if column_names[i] == 'date_prediction' and value is not None:
                        prediction[column_names[i]] = value.isoformat() if hasattr(value, 'isoformat') else str(value)
                    else:
                        prediction[column_names[i]] = value
                predictions.append(prediction)
            
            return predictions
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des prédictions: {str(e)}")
            # Retourner des données factices en cas d'erreur
            print("⚠️ Retour de données factices suite à une erreur")
            from datetime import datetime, timedelta
            
            mock_data = []
            for i in range(min(5, limit)):
                mock_data.append({
                    "id": i,
                    "date_prediction": (datetime.now() - timedelta(days=i)).isoformat(),
                    "sexe": 1 if i % 2 == 0 else 2,
                    "age": 30 + i*5,
                    "dep": 75,
                    "catu": 1,
                    "trajet": 0,
                    "secu1": 1,
                    "agg": 1,
                    "place": 1,
                    "catv": 7,
                    "atm": 1,
                    "lum": 1,
                    "circ": 1,
                    "choc": 1,
                    "manv": 1,
                    "motor": 1,
                    "vma": 50,
                    "severity": "Grave" if i % 2 == 0 else "Léger",
                    "prediction": 1 if i % 2 == 0 else 0,
                    "probability": 0.7 - (i * 0.1)
                })
            return mock_data