import schedule
import time
import os
import sys
import threading
from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import uvicorn

from main import run_etl
from etl.utils import logger

app = FastAPI(
    title="HealthAI ETL Service",
    description="ETL Scheduler and Metrics for HealthAI",
)

@app.get("/metrics", tags=["Monitoring"])
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

def job():
    """Tâche périodique : exécute le pipeline ETL."""
    logger.info("Starting scheduled ETL job...")
    success = run_etl()
    if success:
        logger.info("Scheduled ETL job completed successfully.")
    else:
        logger.error("Scheduled ETL job failed.")

def run_scheduler():
    """
    Lance l'ordonnanceur dans un thread séparé.
    """
    schedule.every().day.at("02:00").do(job)
    logger.info("ETL Scheduler started. Job scheduled for 02:00 daily.")
    
    # Exécution immédiate au démarrage pour vérification
    job()

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    try:
        # Lancer le scheduler dans un thread en arrière-plan
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        
        # Lancer FastAPI sur le port 8000 (thread principal)
        logger.info("Prometheus metrics FastAPI server starting on port 8000.")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        logger.info("Service stopped by user.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Service crashed: {e}")
        sys.exit(1)
