# Utilise une image Python
FROM python:3.10-slim

# Installer sqlite3 CLI et dépendances
RUN apt-get update && \
    apt-get install -y sqlite3 && \
    apt-get clean

# Crée un répertoire de travail
WORKDIR /app

# Copier les fichiers du projet dans le conteneur
COPY api/ ./api/
COPY model/registry/ ./model/registry/
COPY common.py ./common.py
COPY requirements_api.txt ./requirements_api.txt
COPY config.yml ./config.yml
COPY tests/ ./tests/
COPY ./data /app/data

# Installer les dépendances
RUN pip install --upgrade pip && \
    pip install -r requirements_api.txt

# Exposer le port 8000
EXPOSE 8000

# Démarre l'API avec Uvicorn
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]