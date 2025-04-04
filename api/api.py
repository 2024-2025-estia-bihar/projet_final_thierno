from fastapi import FastAPI, HTTPException
import sqlite3
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common import CONFIG

app = FastAPI()

db_path = CONFIG['paths']['db_path']

VALID_HOURS = {"00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"}

@app.get("/date/{date}")
def get_prediction_by_date(date: str):
    """Récupère la prédiction pour une date donnée."""
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM predictions WHERE prediction_date_time LIKE ?"
    df = pd.read_sql(query, conn, params=(date + "%",))
    conn.close()
    
    if df.empty:
        raise HTTPException(status_code=404, detail="Prédiction non trouvée")
    
    df["hour"] = df["prediction_date_time"].str[-5:]  # Extrait HH:MM de la prediction_date_time
    df_filtered = df[df["hour"].isin(VALID_HOURS)]
    
    if df_filtered.empty:
        raise HTTPException(status_code=400, detail="Heure invalide. Utilisez l'une des heures suivantes: 00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00")
    
    return df_filtered[["prediction_date_time", "temperature_pred"]].to_dict(orient="records")

@app.get("/predictions")
def get_all_predictions():
    """Récupère toutes les prédictions."""
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM predictions"
    df = pd.read_sql(query, conn)
    conn.close()
    
    return df.to_dict(orient="records")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
