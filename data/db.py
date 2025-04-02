import sqlite3

# Connexion à la base de données (créée si elle n'existe pas)
conn = sqlite3.connect("ts_meteo.db")
cursor = conn.cursor()

# Création de la table des données météo historiques
cursor.execute("""
CREATE TABLE IF NOT EXISTS weather_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_time DATETIME UNIQUE,
    temperature REAL,
    humidity REAL
)
""")

# Création de la table des métadonnées des modèles
cursor.execute("""
CREATE TABLE IF NOT EXISTS model_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    version TEXT NOT NULL,
    training_start_date DATE NOT NULL,
    training_end_date DATE NOT NULL,
    hyperparameters TEXT,  -- Stocké sous forme de JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Création de la table des prédictions générées
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER,
    prediction_date_time DATETIME,
    temperature_pred REAL,
    FOREIGN KEY (model_id) REFERENCES model_metadata(id)
)
""")

# Sauvegarde et fermeture de la connexion
conn.commit()
conn.close()

print("Base de données SQLite créée avec succès !")