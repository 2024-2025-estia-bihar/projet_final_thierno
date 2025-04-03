import sqlite3
import pickle
import pandas as pd
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common import CONFIG

# Charger le modèle
model_path = CONFIG['paths']['model_path']
with open(model_path, "rb") as f:
    model = pickle.load(f)

# Connexion à la base de données
db_path = CONFIG['paths']['db_path']
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Récupérer l'ID du modèle utilisé
cursor.execute("SELECT id FROM model_metadata ORDER BY training_end_date DESC LIMIT 1")
model_id = cursor.fetchone()
model_id = model_id[0] if model_id else None

# Charger les données de weather_data pour le 25 mars 2025
query = """
SELECT date_time, temperature, humidity
FROM weather_data
WHERE date_time BETWEEN '2025-03-23 12:00:00' AND '2025-03-25 21:00:00'
"""
data = pd.read_sql(query, conn, parse_dates=['date_time'])
data.set_index('date_time', inplace=True)

# Prétraiter les données
lag_end = min(12, len(data))  # Adapter lag_end si peu de données
for i in range(1, lag_end):
    data[f"lag_{i}"] = data['temperature'].shift(i)
data.dropna(inplace=True)

# Ajouter la moyenne par tranche de 3 heures
data["hour_3_interval"] = (data.index.hour // 3)
hourly_average = data.groupby("hour_3_interval")['temperature'].mean().to_dict()
data["hour_3_average"] = data["hour_3_interval"].map(hourly_average)
data.drop(["hour_3_interval"], axis=1, inplace=True)

data.drop(columns=['temperature'], inplace=True, errors='ignore')

# Faire les prédictions
y_pred = model.predict(data)

# Insérer les prédictions dans la table predictions
for date, pred in zip(data.index, y_pred):
    cursor.execute("""
    INSERT INTO predictions (prediction_date_time, temperature_pred, model_id)
    VALUES (?, ?, ?)
    """, (date.strftime("%Y-%m-%d %H:%M:%S"), float(pred), model_id))

conn.commit()
conn.close()

print("Prédictions enregistrées avec succès.")

# # Connexion à la base de données
# db_path = CONFIG['paths']['db_path']
# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()

# # Vider la table predictions
# cursor.execute("DELETE FROM predictions")

# # Confirmer les changements
# conn.commit()
# conn.close()

# print("Table 'predictions' vidée avec succès.")