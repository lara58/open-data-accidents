# Point d'entrée Flask

from flask import Flask
from flask_cors import CORS
from routes.accident_routes import accident_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)
CORS(app)  # autorise les requêtes React depuis localhost:3000

app.register_blueprint(accident_bp, url_prefix="/api/accidents")
app.register_blueprint(auth_bp, url_prefix="/api/auth")

@app.route('/favicon.ico')
def favicon():
    return '', 204  # No Content


if __name__ == "__main__":
    app.run(debug=True, port=5000)
