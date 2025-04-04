from fastapi import FastAPI, HTTPException
import sqlite3
import pandas as pd
import sys
import os
from logger import logger

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common import CONFIG

app = FastAPI()

db_path = CONFIG['paths']['db_path']

VALID_HOURS = {"00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"}

@app.get("/date/{date}")
def get_prediction_by_date(date: str):
    logger.info(f"GET /date/{date} - Récupération des prédictions pour cette date")
    try:
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM predictions WHERE prediction_date_time LIKE ?"
        df = pd.read_sql(query, conn, params=(date + "%",))
        conn.close()
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Prédiction non trouvée")
        
        df["hour"] = df["prediction_date_time"].str[-5:]  # Extrait HH:MM de la prediction_date_time
        df_filtered = df[df["hour"].isin(VALID_HOURS)]
        
        if df_filtered.empty:
            logger.warning(f"Aucune prédiction à une heure valide pour la date {date}")
            raise HTTPException(
                status_code=400,
                detail="Heure invalide. Utilisez l'une des heures suivantes: 00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00"
            )

        logger.info(f"{len(df_filtered)} prédictions retournées pour {date}")
        return df_filtered[["prediction_date_time", "temperature_pred"]].to_dict(orient="records")
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des prédictions pour {date} : {e}")
        raise HTTPException(status_code=404, detail=f"Erreur lors de la récupération des prédictions pour {date} : {e}")

@app.get("/predictions")
def get_all_predictions():
    try :
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM predictions"
        df = pd.read_sql(query, conn)
        conn.close()
        
        logger.info(f"{len(df)} prédictions retournées")
        return df.to_dict(orient="records")

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des prédictions : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")
    
VERSION = "1.0.0"
@app.get("/version", summary="Version actuelle de l'API", tags=["Infos"])
def get_version():
    """Retourne la version actuelle du logiciel déployé."""
    logger.info("GET /version - Récupération de la version du logiciel")
    return {"version": VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
