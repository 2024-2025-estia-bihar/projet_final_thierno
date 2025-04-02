import sys
import os
import sqlite3
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common import CONFIG

def load_data():
    # Récupérer le chemin de la base de données depuis le fichier de config
    db_path = CONFIG['paths']['db_path']
    
    # Connexion à la base de données SQLite
    conn = sqlite3.connect(db_path)
    
    # Charger les données dans un DataFrame
    query = "SELECT * FROM weather_data"
    df = pd.read_sql(query, conn)
    
    # Fermer la connexion
    conn.close()
    
    return df

if __name__ == "__main__":
    data = load_data()
    print(data.head())