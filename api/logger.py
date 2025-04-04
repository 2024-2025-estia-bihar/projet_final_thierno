import logging

# Configuration de base du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log dans un fichier
        logging.StreamHandler()          # Log dans la console
    ]
)

# Création du logger
logger = logging.getLogger("api_logger")