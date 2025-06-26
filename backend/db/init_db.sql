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
    lieu_departement INTEGER NOT NULL, -- obligatoire a envoyer au modele (numerique)
    lieu_commune TEXT,
    lieu_latitude DOUBLE,
    lieu_longitude DOUBLE,
    agglomeration INTEGER NOT NULL,  -- obligatoire a envoyer au modele (numerique)
    type_route INTEGER NOT NULL,  -- obligatoire a envoyer au modele (numerique)
    condition_meteo INTEGER NOT NULL, -- obligatoire a envoyer au modele (numerique)
    luminosite INTEGER NOT NULL,  -- obligatoire a envoyer au modele (numerique)
    collision_type TEXT,
    gravite_accident TEXT,
    gravite_accident_proba TEXT,
    nb_vehicules INTEGER,
    categorie_vehicule INTEGER NOT NULL,  -- obligatoire a envoyer au modele (numerique)
    nb_usagers INTEGER,
    categorie_usager INTEGER NOT NULL,  -- obligatoire a envoyer au modele (numerique)
    age INTEGER NOT NULL,  -- obligatoire a envoyer au modele (numerique)
    motif_deplacement INTEGER NOT NULL,  -- obligatoire a envoyer au modele (numerique)
    equipement_securite INTEGER NOT NULL,  -- obligatoire a envoyer au modele (numerique)
    place_usager INTEGER NOT NULL,  -- obligatoire a envoyer au modele (numerique)
    sexe_usager INTEGER NOT NULL,  -- obligatoire a envoyer au modele (numerique)
    manoeuvre_principal_accident INTEGER NOT NULL,  -- obligatoire a envoyer au modele (numerique)
    type_moteur INTEGER NOT NULL,  -- obligatoire a envoyer au modele (numerique) au modele (numerique)
    vitesse_max INTEGER NOT NULL,  -- obligatoire a envoyer au modele (numerique)
    point_choc_initial INTEGER NOT NULL,  -- obligatoire a envoyer au modele (numerique)
    description TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
