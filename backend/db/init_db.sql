-- Connexion DuckDB

-- Créer la table users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- créer la table accidents avec la foreign key
CREATE TABLE IF NOT EXISTS accidents (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    date_accident DATE NOT NULL,
    heure_accident TEXT,
    lieu_code_insee TEXT,
    lieu_departement TEXT,
    lieu_commune TEXT,
    lieu_latitude DOUBLE,
    lieu_longitude DOUBLE,
    agglomeration TEXT,
    type_route TEXT,
    condition_meteo TEXT,
    luminosite TEXT,
    collision_type TEXT,
    gravite_accident TEXT,
    nb_vehicules INTEGER,
    categorie_vehicule TEXT,
    nb_usagers INTEGER,
    categorie_usager TEXT,
    age INTEGER,
    motif_deplacement TEXT,
    equipement_securite TEXT,
    place_usager TEXT,
    sexe_usager TEXT,
    manoeuvre_principal_accident TEXT,
    type_moteur TEXT,
    vitesse_max INTEGER,
    point_choc_initial TEXT,
    description TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);


