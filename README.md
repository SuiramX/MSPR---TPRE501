# MSPR — Guide d'installation (complet et clair)

Ce document décrit comment installer et lancer le projet en deux modes:

- Mode A (recommandé) : Docker + Docker Compose — reproduit en local PostgreSQL, Prometheus et Grafana.
- Mode B : Exécution locale (venv) — vous gérez PostgreSQL, Prometheus et Grafana séparément.
Ports exposés

- `8000/tcp` — FastAPI (uvicorn)
- `5432/tcp` — PostgreSQL
- `9090/tcp` — Prometheus
- `3000/tcp` — Grafana

Pré-requis

- Git (optionnel)
- Docker + Docker Compose (si vous utilisez les conteneurs)
- Python 3.9 (si exécution locale — le Dockerfile utilise `python:3.9-slim`)
- `pip`, `virtualenv` (exécution locale)

IMPORTANT: adaptez les commandes ci-dessous selon votre OS (Windows vs Linux).

---

Mode A — Docker Compose (rapide & isolé)

1) Cloner le dépôt (si nécessaire) :

```bash
git clone https://github.com/SuiramX/MSPR---TPRE501.git
cd MSPR---TPRE501
```

2) Démarrer tous les services :

```bash
docker-compose up --build -d
```

Accès après démarrage (exemples) :

- FastAPI: http://localhost:8000/
- Prometheus UI: http://localhost:9090/
- Grafana: http://localhost:3000/ (admin/admin)

Notes Docker

- Service `app` construit depuis `app/Dockerfile` et expose `8000`.
- PostgreSQL : utilisateur `user`, mot de passe `password`, base `mspr`. Le premier démarrage exécute `init.sql`.
- Prometheus : configuré via `prometheus/prometheus.yml` monté dans le conteneur.
- Grafana : accès web sur le port `3000` (identifiants par défaut Grafana : `admin`/`admin` — changez le mot de passe au premier lancement).



---

Mode B — Exécution locale (venv)

1) Préparez un environnement virtuel

Linux / macOS :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r app/requirements.txt
```

Windows (PowerShell) :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r app\requirements.txt
```

2) PostgreSQL

- Option A (local): installez PostgreSQL et créez la base `mspr` :

```sql
-- en psql
CREATE USER "user" WITH PASSWORD 'password';
CREATE DATABASE mspr OWNER "user";
```

Appliquer le script d'initialisation :

```bash
psql -h localhost -U user -d mspr -f init.sql
```

- Option B (conteneur si vous ne voulez pas installer PostgreSQL localement) :

```bash
docker run -d --name mspr-db \
  -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=mspr \
  -p 5432:5432 -v "$PWD/postgres_data":/var/lib/postgresql/data postgres:15
```

3) Variables d'environnement

Exportez `DATABASE_URL` (exemples) :

Linux / macOS:

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/mspr"
```

Windows PowerShell:

```powershell
$env:DATABASE_URL = "postgresql://user:password@localhost:5432/mspr"
```

4) Lancer l'application

```bash
cd app
uvicorn main:app --host 0.0.0.0 --port 8000
```

Accès:

- FastAPI: http://localhost:8000/

---

Pare-feu — ouverture des ports (exemples)

Windows (PowerShell en administrateur) :

```powershell
netsh advfirewall firewall add rule name="MSPR App 8000" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="MSPR Postgres 5432" dir=in action=allow protocol=TCP localport=5432
netsh advfirewall firewall add rule name="Prometheus 9090" dir=in action=allow protocol=TCP localport=9090
netsh advfirewall firewall add rule name="Grafana 3000" dir=in action=allow protocol=TCP localport=3000
```

Linux (Ubuntu + ufw) :

```bash
sudo ufw allow 8000/tcp
sudo ufw allow 5432/tcp
sudo ufw allow 9090/tcp
sudo ufw allow 3000/tcp
sudo ufw reload
```

---

Vérifications & dépannage rapide

- Voir logs Docker :

```bash
docker-compose logs -f app
docker logs mspr-db   # pour PostgreSQL container
```

- En local : vérifier que `DATABASE_URL` est correct et que Postgres écoute sur `localhost:5432`.
- Si l'application ne démarre pas, relancer `uvicorn` avec `--reload` pour voir les erreurs.

Points spécifiques Prometheus / Grafana

- Prometheus lit sa config depuis `prometheus/prometheus.yml` (monté via Docker Compose).
- Grafana stocke ses données dans le volume `grafana_data` défini dans `docker-compose.yml`. Par défaut Grafana user/password = `admin`/`admin`.

Commandes récapitulatives

```bash
# Docker (recommandé)
docker-compose up --build -d
docker-compose ps
docker-compose logs -f app
docker-compose down

# Local
python -m venv .venv
source .venv/bin/activate   # ou .\.venv\Scripts\Activate.ps1
pip install -r app/requirements.txt
export DATABASE_URL="postgresql://user:password@localhost:5432/mspr"
cd app && uvicorn main:app --reload --port 8000
```

Annexes

- Fichier d'initialisation SQL: [init.sql](init.sql)
- Fichier Docker Compose: [docker-compose.yml](docker-compose.yml)

Si vous voulez que je :

- lance les containers ici (`docker-compose up --build -d`),
- ajoute un script d'initialisation pour Grafana (datasource / dashboard provisioning), ou
- génère un service systemd ou un fichier `docker-compose.override.yml` personnalisé,

dites-moi lequel et je l'ajoute.


