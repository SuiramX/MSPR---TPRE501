FROM python:3.9-slim

WORKDIR /app

# Installation des dépendances système si nécessaire (ex: cron n'est pas utilisé ici car on utilise scheduler.py)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# L'entrypoint est défini dans le docker-compose via la commande
CMD ["python", "scheduler.py"]
