import os
import sys
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration essentielle pour contourner l'erreur de sécurité
os.environ['HADOOP_USER_NAME'] = 'hadoop'
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
os.environ['JAVA_OPTS'] = '-Djavax.security.auth.useSubjectCredsOnly=false'
os.environ['PYSPARK_SUBMIT_ARGS'] = '--conf spark.ui.enabled=false --conf spark.hadoop.fs.defaultFS=file:/// --conf spark.authenticate=false --conf spark.security.credentials.kubernetes.enabled=false pyspark-shell'

from flask import Flask, jsonify
from flask_cors import CORS
from routes.accident_routes import accident_bp
from routes.prediction_routes import prediction_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)
# Activer CORS pour permettre au frontend de communiquer avec l'API
CORS(app)

# Enregistrer les blueprints pour les routes API
app.register_blueprint(accident_bp, url_prefix="/api/accidents")
app.register_blueprint(prediction_bp, url_prefix="/api/predictions")
app.register_blueprint(auth_bp, url_prefix="/api/auth")

@app.route('/')
def index():
    return jsonify({"message": "API des accidents et prédictions opérationnelle"})

@app.route('/api/status')
def status():
    """Vérifier l'état du modèle"""
    from services.prediction_service import is_model_loaded
    return jsonify({
        "model_loaded": is_model_loaded(),
        "model_type": "PySpark Random Forest",
        "status": "operational" if is_model_loaded() else "error"
    })

# Garder la route mock pour les tests si nécessaire
@app.route('/mock-predictions')
def mock_predictions():
    """Données mockées pour les tests frontend"""
    return jsonify([
        {
            "id": 1,
            "date_prediction": "2023-08-15T14:30:00",
            "dep": 75,
            "severity": "Léger",
            "probability": 0.3,
            "latitude": 48.856614,
            "longitude": 2.3522219,
            "sexe": 1,
            "age": 30,
            "catv": 7,
            "place": 1,
            "agg": 1,
            "lum": 1,
            "vma": 50,
            "trajet": 1
        },
        {
            "id": 2,
            "date_prediction": "2023-08-14T10:15:00",
            "dep": 69,
            "severity": "Grave",
            "probability": 0.7,
            "latitude": 45.750000,
            "longitude": 4.850000,
            "sexe": 2,
            "age": 45,
            "catv": 33,
            "place": 2,
            "agg": 0,
            "lum": 3,
            "vma": 90,
            "trajet": 3
        }
    ])

if __name__ == "__main__":
    app.run(debug=True)