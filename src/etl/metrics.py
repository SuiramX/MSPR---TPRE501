from prometheus_client import Counter, Gauge, Summary

# Métriques pour le suivi de l'ETL
ETL_JOB_DURATION = Gauge('etl_job_duration_seconds', 'Temps pris par la dernière exécution de l\'ETL')
ETL_JOB_STATUS = Gauge('etl_job_status', 'Statut de l\'ETL (1: succès, 0: échec, 2: en cours)')
ETL_JOB_FAILURES = Counter('etl_job_failures_total', 'Nombre total d\'échecs de l\'ETL')
ETL_JOB_LAST_SUCCESS = Gauge('etl_job_last_success_timestamp_seconds', 'Horodatage du dernier succès de l\'ETL')
