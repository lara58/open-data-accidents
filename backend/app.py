from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'message': 'API Flask fonctionne !'})

@app.route('/accidents')
def get_accidents():
    accidents = [
        {"id": 1, "ville": "Paris", "gravite": "Blessé léger", "date": "2023-01-10"},
        {"id": 2, "ville": "Lyon", "gravite": "Tué", "date": "2023-02-18"},
        {"id": 3, "ville": "Marseille", "gravite": "Blessé grave", "date": "2023-03-25"}
    ]
    return jsonify(accidents)

if __name__ == '__main__':
    app.run(debug=True)
