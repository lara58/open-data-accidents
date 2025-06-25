-- Connexion DuckDB

-- Table users (
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- Table accidents 
CREATE TABLE IF NOT EXISTS accidents (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    date_accident DATE NOT NULL,
    heure_accident TEXT,
    lieu_code_insee TEXT,
    lieu_departement INTEGER NOT NULL, -- obligatoire (numerique)
    lieu_commune TEXT,
    lieu_latitude DOUBLE,
    lieu_longitude DOUBLE,
    agglomeration INTEGER NOT NULL, -- obligatoire (numerique)
    type_route INTEGER NOT NULL, -- obligatoire (numerique)
    condition_meteo INTEGER NOT NULL, -- obligatoire (numerique)
    luminosite INTEGER NOT NULL, -- obligatoire (numerique)
    collision_type TEXT,
    gravite_accident TEXT,
    nb_vehicules INTEGER,
    categorie_vehicule INTEGER NOT NULL, -- obligatoire (numerique)
    nb_usagers INTEGER,
    categorie_usager INTEGER NOT NULL, -- obligatoire (numerique)
    age INTEGER NOT NULL, -- obligatoire (numerique)
    motif_deplacement INTEGER NOT NULL, -- obligatoire (numerique)
    equipement_securite INTEGER NOT NULL, -- obligatoire (numerique)
    place_usager INTEGER NOT NULL, -- obligatoire (numerique)
    sexe_usager INTEGER NOT NULL, -- obligatoire (numerique)
    manoeuvre_principal_accident INTEGER NOT NULL, -- obligatoire (numerique)
    type_moteur INTEGER NOT NULL, -- obligatoire (numerique)
    vitesse_max INTEGER NOT NULL, -- obligatoire (numerique)
    point_choc_initial INTEGER NOT NULL, -- obligatoire (numerique)
    description TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
