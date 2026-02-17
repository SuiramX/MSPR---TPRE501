import schedule
import time
import os
import sys
from main import run_etl
from etl.utils import logger

def job():
    """Tâche périodique : exécute le pipeline ETL."""
    logger.info("Starting scheduled ETL job...")
    success = run_etl()
    if success:
        logger.info("Scheduled ETL job completed successfully.")
    else:
        logger.error("Scheduled ETL job failed.")

def main():
    """
    Initialise l'ordonnanceur (scheduler).
    Configure une exécution quotidienne à 02:00.
    """
    # Planification : une fois par jour à 2h du matin
    schedule.every().day.at("02:00").do(job)
    
    logger.info("ETL Scheduler started. Job scheduled for 02:00 daily.")
    
    # Exécution immédiate au démarrage pour vérification
    job()

    # Boucle infinie pour maintenir le scheduler actif
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Scheduler crashed: {e}")
        sys.exit(1)
