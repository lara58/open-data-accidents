-- Connexion DuckDB

CREATE TABLE IF NOT EXISTS accidents (
    id INTEGER PRIMARY KEY,
    date DATE,
    location TEXT,
    severity TEXT,
    year INTEGER
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
