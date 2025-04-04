# < Project name >
High-level description

Data flow & architecture

Main technologies used and for which purpose

# Running locally
Instructions to install dependencies, run, build, test

# CI/CD steps
Short description of each step with their outputs (if any)

db.py
download.py
load_data.py
train.py
predictions.py
api.py

# Déploiement de l’API météo avec Docker
    -   Construction de l’image Docker

Assurez-vous d’être à la racine du projet (projet_final_thierno/), puis exécutez : docker-compose build.

Cela construit une image Docker contenant : Python 3.10, FastAPI, Uvicorn, Pandas, PyYAML et le fichier ts_meteo.db monté comme volume, le modèle et les fichiers de configuration.

    -   Lancement du conteneur : docker-compose up -d
    -   Arrêt : docker-compose down
    -   Tester les endpoints : 

Liste des prédictions
GET http://localhost:8000/predictions

Prédictions par date :
GET http://localhost:8000/date/2025-03-25
(Heures valides : 00:00, 03:00, ..., 21:00)
