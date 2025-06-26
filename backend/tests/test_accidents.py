import json
import pytest
from app import app  # Assure-toi que l'instance Flask s'appelle `app`

# Utilisateur factice avec un token simulé
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer faketoken123"  # Doit correspondre à ton système de token mocké
}

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_enregistrer_accident(client):
    data = {
        "mois": 6,
        "jour": 1,
        "lieu_code_insee": "75056",
        "lieu_departement": "75",
        "lieu_commune": "Paris",
        "lieu_latitude": 48.8566,
        "lieu_longitude": 2.3522,
        "agglomeration": "Oui",
        "type_route": "Urbain",
        "condition_meteo": "Pluie",
        "luminosite": "Jour",
        "collision_type": "Choc frontal",
        "gravite_accident": "Grave",
        "nb_vehicules": 2,
        "categorie_vehicule": "Voiture",
        "nb_usagers": 3,
        "categorie_usager": "Conducteur",
        "age": 34,
        "motif_deplacement": "Travail",
        "equipement_securite": "Ceinture",
        "place_usager": "Avant",
        "sexe_usager": "Homme",
        "manoeuvre_principal_accident": "Dépassement",
        "type_moteur": "Thermique",
        "vitesse_max": 130,
        "point_choc_initial": "Avant",
        "description": "Test accident grave à Paris"
    }

    response = client.post("/api/accidents/", headers=HEADERS, data=json.dumps(data))
    assert response.status_code == 201
    assert "Accident enregistré avec succès" in response.get_data(as_text=True)

def test_lister_accidents(client):
    response = client.get("/api/accidents/", headers=HEADERS)
    assert response.status_code == 200
    accidents = response.get_json().get("accidents", [])
    assert isinstance(accidents, list)

def test_lire_accident_par_id(client):
    # Suppose que l'accident avec l'ID 1 existe
    response = client.get("/api/accidents/1", headers=HEADERS)
    if response.status_code == 200:
        accident = response.get_json()
        assert "id" in accident
    else:
        assert response.status_code == 404
