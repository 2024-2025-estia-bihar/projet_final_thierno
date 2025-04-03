import pandas as pd
import numpy as np
import pickle
import sqlite3
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import sys
import os

from load_data import load_data

# Chargement du fichier config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common import CONFIG  # Assurez-vous que 'common.py' contient bien le chargement de CONFIG

def preprocess_data(data, lag_start=1, lag_end=8, test_size=0.15):
    """Prétraitement des données pour la prédiction des séries temporelles"""
    data = pd.DataFrame(data.copy())

    data.index = pd.to_datetime(data.index)

    # Ajouter des décalages temporels comme features
    for i in range(lag_start, lag_end):
        data[f"lag_{i}"] = data['temperature'].shift(i)

    # Supprimer les NaNs générés par le décalage
    data.dropna(inplace=True)

    # Ajouter une colonne pour regrouper par intervalle de 3 heures
    data["hour_3_interval"] = (data.index.hour // 3)  # Divise l'heure en intervalles de 3h

    X = data.drop('temperature', axis=1)
    y = data['temperature']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=False)

    # Calculer la moyenne des valeurs sur les intervalles de 3 heures (uniquement sur train)
    hourly_average = data.loc[X_train.index].groupby("hour_3_interval")['temperature'].mean().to_dict()
    X_train["hour_3_average"] = X_train["hour_3_interval"].map(hourly_average)
    X_test["hour_3_average"] = X_test["hour_3_interval"].map(hourly_average)

    # Supprimer la colonne "hour_3_interval"
    X_train.drop(["hour_3_interval"], axis=1, inplace=True)
    X_test.drop(["hour_3_interval"], axis=1, inplace=True)

    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    """Entraîne un modèle de régression linéaire"""
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Évalue le modèle et affiche la courbe des prédictions"""
    y_pred = model.predict(X_test)
    score = r2_score(y_test, y_pred)

    print(score)

    return score

def persist_model(model, X_train, config):
    """Sauvegarde le modèle et les métadonnées dans SQLite"""
    model_version = "2.0"
    model_name = "linear_regression" 
    train_start = X_train.index.min().strftime("%Y-%m-%d %H:%M:%S")
    train_end = X_train.index.max().strftime("%Y-%m-%d %H:%M:%S")

    # Connexion à la base de données SQLite
    db_path = config['paths']['db_path']
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insérer les métadonnées dans la table model_metadata
    cursor.execute("""
        INSERT INTO model_metadata (model_name, version, training_start_date, training_end_date, hyperparameters)
        VALUES (?, ?, ?, ?, ?)
    """, (model_name, model_version, train_start, train_end, str(model.get_params())))

    conn.commit()
    conn.close()

    # Sauvegarde du modèle avec pickle
    model_path = config['paths']['model_path']
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

# Charger les données jusqu'au 2025-03-24 inclus
df = load_data()
df = df[df['date_time'] <= '2025-03-24']

# Sélectionner les colonnes pertinentes
ts_meteo = df[['temperature', 'humidity']].copy()
ts_meteo.index = df['date_time'] 

# Prétraitement
X_train, X_test, y_train, y_test = preprocess_data(ts_meteo, lag_end=12)

# Entraînement du modèle
model = train_model(X_train, y_train)

# Évaluation
evaluate_model(model, X_test, y_test)

# Sauvegarde du modèle et des métadonnées
persist_model(model, X_train, CONFIG)