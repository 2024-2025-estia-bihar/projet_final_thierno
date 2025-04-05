# Projet Final - API de Prédiction Météo

Ce projet expose un modèle de machine learning sous forme d'API REST avec FastAPI.  
Il permet de prédire des températures à différents moments d'une journée donnée à partir de données météo.

---

## Data flow & Architecture

Le projet est structuré en plusieurs étapes pour gérer un pipeline complet de ML :

1. **Téléchargement et préparation des données** : `download.py` et `load_data.py`
2. **Entraînement du modèle** : `train.py`
3. **Prédiction périodique** : `predictions.py`
4. **Stockage des résultats** : base de données SQLite (`ts_meteo.db`)
5. **Exposition du modèle via une API** : `api.py` (FastAPI)
6. **Logs et suivi des erreurs** : `logger.py`
7. **Tests des endpoints** : `test_api.py`

---

## Technologies principales

| Technologie     | Rôle                                  |
|------------------|---------------------------------------|
| Python           | Langage principal                     |
| FastAPI          | Création de l'API REST                |
| SQLite           | Base de données locale                |
| Pandas           | Manipulation de données               |
| PyYAML           | Chargement des fichiers de config     |
| Uvicorn          | Serveur ASGI pour FastAPI             |
| Docker           | Conteneurisation de l’application     |
| GitHub Actions   | CI/CD automatisé                      |

---

## Lancer le projet en local

### 1. Installation

```bash
git clone <repo-url>
cd projet_final_thierno
pip install -r requirements.txt
```

### 2. Lancement de l’API

```bash
uvicorn api:app --reload
```

L’API sera disponible à [http://localhost:8000](http://localhost:8000)

---

## Déploiement avec Docker

- **Construction de l’image** :
  ```bash
  docker-compose build
  ```

- **Lancement du conteneur** :
  ```bash
  docker-compose up -d
  ```

- **Arrêt** :
  ```bash
  docker-compose down
  ```

---

## CI/CD (GitHub Actions)

| Étape CI/CD            | Description                                                      |
|------------------------|------------------------------------------------------------------|
| Build image Docker     | Construit l’image à partir du `Dockerfile`                      |
| Push vers GHCR         | Envoie l’image sur `ghcr.io`                                    |
| Run tests              | Exécute `pytest` dans le conteneur                              |
| Deploy (optionnel)     | Déploiement automatique (si configuré)                          |

---

## Fichiers principaux

| Fichier         | Description                                                                 |
|------------------|----------------------------------------------------------------------------|
| `db.py`          | Gestion de la base SQLite                                                  |
| `download.py`    | Téléchargement initial des données                                         |
| `load_data.py`   | Chargement des données au format pandas                                   |
| `train.py`       | Entraînement et sauvegarde du modèle                                      |
| `predictions.py` | Génération périodique des prédictions (batch)                             |
| `api.py`         | Implémentation de l'API avec FastAPI                                      |
| `logger.py`      | Logging personnalisé pour l'API                                            |
| `test_api.py`    | Tests des endpoints API avec `pytest`                                     |

---

## Documentation des endpoints

> URL de base : `http://localhost:8000`

### 1. `GET /date/{date}`

Récupère les prédictions pour une date donnée.

- **Paramètre** : `date` au format `YYYY-MM-DD`
- **Réponses** :
  - `200 OK` : liste d'objets `{ prediction_date_time, temperature_pred }`
  - `404 Not Found` : "Prédiction non trouvée"

### 2. `GET /predictions`

Récupère toutes les prédictions de la base.

- **Réponses** :
  - `200 OK` : liste complète des prédictions
  - `404 Not Found` : si aucune donnée n'est disponible

### 3. `GET /version`

Retourne la version actuelle du service.

- **Réponse** :
  - `200 OK` : version sous forme de chaîne (ex: `"v1.0.0"`)

---

## Tester les endpoints

Depuis le dossier `projet_final_thierno/api` :

```bash
pytest test_api.py
```

---

## Structure modulaire du code

Ce projet respecte une **séparation claire des responsabilités** :

- **Prétraitement** : découplé dans `load_data.py`
- **Entraînement** : centralisé dans `train.py`
- **Prédiction** : exécuté en batch avec `predictions.py`
- **API** : FastAPI encapsule tout le pipeline (prétraitement + prédiction)
- **Expérimentation/versionnement** : les modèles sont sauvegardés avec horodatage, facilitant le suivi

---

## Versionnement des modèles

Chaque modèle entraîné est sauvegardé avec un nom incluant la date (`model_YYYYMMDD.pkl`) pour gérer le **versioning manuel**.  
Un système d’amélioration pourrait consister à intégrer MLflow ou DVC pour automatiser cela.

---