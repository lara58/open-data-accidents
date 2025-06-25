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
    lieu_departement TEXT, --dep obligatoire pour la prediction (non numerique) 
    lieu_commune TEXT,
    lieu_latitude DOUBLE,
    lieu_longitude DOUBLE,
    agglomeration TEXT, --agg obligatoire pour la prediction (non numerique)
    type_route TEXT, --circ obligatoire pour la prediction (numerique)
    condition_meteo TEXT, --atm obligatoire pour la prediction (numerique)
    luminosite TEXT, --lum obligatoire pour la prediction (numerique)
    collision_type TEXT,
    gravite_accident TEXT,
    nb_vehicules INTEGER,
    categorie_vehicule TEXT, --catv obligatoire pour la prediction (numerique)
    nb_usagers INTEGER,
    categorie_usager TEXT,--catu obligatoire pour la prediction (non numerique)
    age INTEGER, --age obligatoire pour la prediction (numerique)
    motif_deplacement TEXT, -- trajet obligatoire pour la prediction (non numerique)
    equipement_securite TEXT, --secu1 obligatoire pour la prediction (non numerique)
    place_usager TEXT, --place obligatoire pour la prediction (numerique)
    sexe_usager TEXT, --sexe obligatoire pour la prediction (non numerique)
    manoeuvre_principal_accident TEXT, -- manv obligatoire pour la prediction (numerique)
    type_moteur TEXT, --motor obligatoire pour la prediction (numerique)
    vitesse_max INTEGER, --vma obligatoire pour la prediction (numerique)
    point_choc_initial TEXT, --choc obligatoire pour la prediction (numerique)
    description TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);


