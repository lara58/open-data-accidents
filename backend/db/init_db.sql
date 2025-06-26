-- Supprimer les tables si elles existent déjà
DROP TABLE IF EXISTS predictions;
DROP TABLE IF EXISTS accidents;
DROP TABLE IF EXISTS users;

-- Créer la table users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- Créer la table accidents avec la foreign key
CREATE TABLE IF NOT EXISTS accidents (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    mois INTEGER NOT NULL,
    jour INTEGER NOT NULL,
    
    -- Informations géographiques (utilisées par le frontend mais pas le modèle)
    lieu_departement TEXT,      -- Correspond à 'dep' dans predictions
    lieu_commune TEXT,
    lieu_latitude DOUBLE,       -- Pour l'affichage sur la carte
    lieu_longitude DOUBLE,      -- Pour l'affichage sur la carte
    
    -- Caractéristiques d'accident (format descriptif pour l'interface)
    agglomeration TEXT,         -- Correspond à 'agg' dans predictions
    type_route TEXT,            -- Correspond à 'circ' dans predictions
    condition_meteo TEXT,       -- Correspond à 'atm' dans predictions
    luminosite TEXT,            -- Correspond à 'lum' dans predictions
    collision_type TEXT,        
    gravite_accident TEXT,      -- Résultat observé (vs 'severity' prédite)
    
    -- Informations du véhicule (format descriptif)
    categorie_vehicule TEXT,    -- Correspond à 'catv' dans predictions
    type_moteur TEXT,           -- Correspond à 'motor' dans predictions
    vitesse_max INTEGER,        -- Correspond à 'vma' dans predictions
    point_choc_initial TEXT,    -- Correspond à 'choc' dans predictions
    
    -- Informations de l'usager (format descriptif)
    categorie_usager TEXT,      -- Correspond à 'catu' dans predictions
    age INTEGER,                -- Correspond à 'age' dans predictions
    motif_deplacement TEXT,     -- Correspond à 'trajet' dans predictions
    equipement_securite TEXT,   -- Correspond à 'secu1' dans predictions
    place_usager TEXT,          -- Correspond à 'place' dans predictions
    sexe_usager TEXT,           -- Correspond à 'sexe' dans predictions
    
    -- Détails supplémentaires
    manoeuvre_principal_accident TEXT,  -- Correspond à 'manv' dans predictions
    nb_vehicules INTEGER,
    nb_usagers INTEGER,
    description TEXT,           -- Commentaire libre
    
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Créer la table des prédictions (format numérique pour le modèle)
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY,
    date_prediction TIMESTAMP NOT NULL,  -- Pour l'historique (frontend)
    
    -- Champs utilisés par le modèle ML
    dep INTEGER NOT NULL,       -- Département
    agg INTEGER NOT NULL,       -- Agglomération (0/1)
    circ INTEGER NOT NULL,      -- Type de route
    atm INTEGER NOT NULL,       -- Condition météo
    lum INTEGER NOT NULL,       -- Luminosité
    catv INTEGER NOT NULL,      -- Catégorie véhicule
    catu INTEGER NOT NULL,      -- Catégorie usager
    age INTEGER NOT NULL,       -- Âge
    trajet INTEGER NOT NULL,    -- Motif déplacement
    secu1 INTEGER NOT NULL,     -- Équipement sécurité
    place INTEGER NOT NULL,     -- Place dans le véhicule
    sexe INTEGER NOT NULL,      -- Sexe
    manv INTEGER NOT NULL,      -- Manœuvre
    motor INTEGER NOT NULL,     -- Type moteur
    vma INTEGER NOT NULL,       -- Vitesse max autorisée
    choc INTEGER NOT NULL,      -- Point de choc
    
    -- Résultats de prédiction
    severity TEXT NOT NULL,     -- Gravité prédite
    probability REAL NOT NULL,  -- Confiance de la prédiction
    
    -- Champs pour le frontend
    latitude REAL,              -- Pour l'affichage sur carte
    longitude REAL,             -- Pour l'affichage sur carte
    accident_id INTEGER,        -- Pour lier à un accident existant
    user_id INTEGER             -- Pour filtrer par utilisateur
);

-- Table pour les statistiques
CREATE TABLE IF NOT EXISTS accident_stats (
    id INTEGER PRIMARY KEY,
    stat_date TIMESTAMP NOT NULL,
    dep INTEGER NOT NULL,
    total_accidents INTEGER NOT NULL,
    severe_accidents INTEGER NOT NULL,
    light_accidents INTEGER NOT NULL
);

-- IMPORTANT: AJOUTER LES IDs EXPLICITES dans les insertions
INSERT INTO users (id, username, email, password) VALUES 
    (1, 'admin', 'admin@example.com', 'password123'),
    (2, 'user1', 'user1@example.com', 'password123');

-- Ajouter ID explicite pour l'accident
INSERT INTO accidents (
    id, user_id, mois, jour, lieu_departement, lieu_commune,
    lieu_latitude, lieu_longitude, agglomeration, type_route, condition_meteo,
    luminosite, categorie_vehicule, categorie_usager, age, motif_deplacement,
    equipement_securite, place_usager, sexe_usager, manoeuvre_principal_accident,
    type_moteur, vitesse_max, point_choc_initial, gravite_accident
) VALUES
    (1, 1, 8, 15, '75', 'Paris', 48.8566, 2.3522, 'En agglomération', 'A sens unique', 'Normale',
    'Plein jour', 'VL seul', 'Conducteur', 30, 'Domicile – travail',
    'Ceinture', 'Conducteur', 'Masculin', 'Sans changement de direction',
    'Hydrocarbures', 50, 'Avant', 'Blessé léger');

-- Ajouter IDs explicites pour les prédictions
INSERT INTO predictions (
    id, date_prediction, dep, agg, circ, atm, lum, catv, catu, age,
    trajet, secu1, place, sexe, manv, motor, vma, choc, severity, probability,
    latitude, longitude
) VALUES 
    (1, CURRENT_TIMESTAMP, 75, 1, 1, 1, 1, 7, 1, 30, 1, 1, 1, 1, 1, 1, 50, 1, 'Léger', 0.3, 48.856614, 2.3522219),
    (2, CURRENT_TIMESTAMP - INTERVAL '1 day', 69, 0, 2, 1, 3, 7, 1, 45, 1, 1, 1, 1, 1, 1, 90, 1, 'Grave', 0.7, 45.750000, 4.850000),
    (3, CURRENT_TIMESTAMP - INTERVAL '2 days', 33, 1, 1, 2, 1, 33, 1, 25, 5, 2, 1, 1, 1, 1, 50, 1, 'Grave', 0.8, 44.837789, -0.579180);