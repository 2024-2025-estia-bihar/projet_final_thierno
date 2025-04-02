import openmeteo_requests
import requests_cache
import sqlite3
import pandas as pd
from retry_requests import retry

# Connexion à la base SQLite
conn = sqlite3.connect("ts_meteo.db")
cursor = conn.cursor()

# Configuration de la requête Open-Meteo avec cache et retry
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Paramètres de l'API Open-Meteo
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 43.26,
    "longitude": 1.34,
    "start_date": "2025-01-24",
    "end_date": "2025-03-25",  # Inclut les données de test
    "hourly": ["temperature_2m", "relative_humidity_2m"],
    "timezone": "Europe/Berlin"
}

# Appel de l'API
responses = openmeteo.weather_api(url, params=params)
response = responses[0]  # Première localisation

# Extraction des données
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()

# Création d'un DataFrame Pandas
hourly_dataframe = pd.DataFrame({
    "date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ),
    "temperature": hourly_temperature_2m,
    "humidity": hourly_relative_humidity_2m
})

# Agrégation par pas de 3 heures
hourly_dataframe.set_index("date", inplace=True)
aggregated_data = hourly_dataframe.resample("3h").mean()
aggregated_data.reset_index(inplace=True)

# Insertion dans la base de données SQLite
aggregated_data.to_sql("ts_meteo", conn, if_exists="append", index=False)

# Fermeture de la connexion
conn.commit()
conn.close()

print(f"Données météo agrégées et insérées ({len(aggregated_data)} lignes).")