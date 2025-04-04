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

# Domention des endpoints

- url de base : http://localhost:8000
- Endpoints :

    1. GET/date/{date}

Récupère les prédictions pour une date donnée.
date (chemin) : La date pour laquelle les prédictions doivent être récupérées. Le format attendu est YYYY-MM-DD.
    - Code HTTP 200 : Si des prédictions sont trouvées pour la date donnée, l'API retourne une liste d'objets avec prediction_date_time et temperature_pred
    - Code HTTP 404 : Si aucune prédiction n'est trouvée pour cette date.

    2. GET/predictions

Récupère toutes les prédictions présentes dans la base de données.
    - Code HTTP 200 : Si des prédictions sont présentes dans la base de données, l'API retourne une liste de toutes les prédictions disponibles.
    - Code HTTP 404 : Si aucune prédiction n'est trouvée pour cette date.

    3. GET /version
Retourne la version actuelle du logiciel déployé.
    - Code HTTP 200 : Retourne la version de l'API sous forme de chaîne de caractères.

# Déploiement de l’API météo avec Docker
    -   Construction de l’image Docker : Assurez-vous d’être à la racine du projet (projet_final_thierno/), puis exécutez : docker-compose build.
Cela construit une image Docker contenant : Python 3.10, FastAPI, Uvicorn, Pandas, PyYAML et le fichier ts_meteo.db monté comme volume, le modèle et les fichiers de configuration.
    -   Lancement du conteneur : docker-compose up -d
    -   Arrêt : docker-compose down
    -   Tester les endpoints
