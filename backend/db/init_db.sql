-- Connexion DuckDB

CREATE TABLE IF NOT EXISTS accidents (
    id INTEGER PRIMARY KEY,
    date DATE,
    location TEXT,
    severity TEXT,
    year INTEGER
);
