MSPR - Guide d'installation

Ce document décrit un guide d'installation complet pour exécuter le projet sur Windows ou Linux, en local (venv) ou avec Docker / Docker Compose. Il inclut les ports exposés, commandes utiles et instructions pour la base de données PostgreSQL, Prometheus et Grafana.

**Prérequis**

- Git (optionnel)
- Docker et Docker Compose (si vous utilisez les conteneurs)
- Python 3.9 (le Dockerfile utilise `python:3.9-slim`) si vous exécutez l'application localement
- `pip` et `virtualenv` (si exécution locale)
- Accès administrateur si vous devez ouvrir des ports dans le pare-feu

**Fichiers importants**

- [docker-compose.yml](docker-compose.yml)
- [app/Dockerfile](app/Dockerfile)
- [app/main.py](app/main.py)
- [app/requirements.txt](app/requirements.txt)
- [init.sql](init.sql)

**Ports exposés**

- 8000/tcp — application FastAPI (uvicorn)
- 5432/tcp — PostgreSQL
- 9090/tcp — Prometheus
- 3000/tcp — Grafana

Installation et exécution
-------------------------

1) Option recommandée : Docker + Docker Compose (Windows et Linux)

Privilèges : installez Docker Desktop sur Windows ou Docker Engine + Docker Compose sur Linux.

Commandes (depuis la racine du projet) :

```bash
docker-compose up --build -d
```

Vérifier les conteneurs et logs :

```bash
docker-compose ps
docker-compose logs -f app
```

Arrêter et supprimer :

```bash
docker-compose down
```

Notes Docker :
- Le service `app` est construit à partir de `app/Dockerfile` et écoute sur le port `8000`.
- PostgreSQL est configuré par `docker-compose.yml` (utilisateur: `user`, mot de passe: `password`, DB: `mspr`) et charge `init.sql` pour initialiser la base.

2) Option locale (sans Docker) — Windows et Linux

Prérequis : Python 3.9 installé, PostgreSQL (ou utiliser un conteneur PostgreSQL séparé).

Sous Linux / macOS (bash) :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r app/requirements.txt
```

Sous Windows (PowerShell) :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r app\requirements.txt
```

Configuration de la base PostgreSQL :

- Soit installez PostgreSQL localement et créez la base `mspr` avec l'utilisateur précisé, soit lancez rapidement Postgres en conteneur :

```bash
docker run -d --name mspr-db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=mspr -p 5432:5432 -v "$PWD/postgres_data":/var/lib/postgresql/data postgres:15
```

Ensuite, pour appliquer `init.sql` (si vous avez Postgres local ou en conteneur) :

```bash
psql -h localhost -U user -d mspr -f init.sql
```

Lancer l'application localement :

```bash
cd app
uvicorn main:app --host 0.0.0.0 --port 8000
```

3) Variables d'environnement

- Le projet attend une variable `DATABASE_URL` au format :

```
postgresql://user:password@db:5432/mspr
```

- En local, adaptez `db` en `localhost` si vous utilisez PostgreSQL local.

4) Pare-feu / ouverture des ports

Windows (PowerShell, en tant qu'administrateur) :

```powershell
# Autoriser le port 8000
netsh advfirewall firewall add rule name="MSPR App 8000" dir=in action=allow protocol=TCP localport=8000
# PostgreSQL
netsh advfirewall firewall add rule name="MSPR Postgres 5432" dir=in action=allow protocol=TCP localport=5432
# Prometheus
netsh advfirewall firewall add rule name="Prometheus 9090" dir=in action=allow protocol=TCP localport=9090
# Grafana
netsh advfirewall firewall add rule name="Grafana 3000" dir=in action=allow protocol=TCP localport=3000
```

Linux (Ubuntu avec `ufw`) :

```bash
sudo ufw allow 8000/tcp
sudo ufw allow 5432/tcp
sudo ufw allow 9090/tcp
sudo ufw allow 3000/tcp
sudo ufw reload
```

Si vous utilisez `firewalld` (CentOS/RHEL) :

```bash
sudo firewall-cmd --add-port=8000/tcp --permanent
sudo firewall-cmd --add-port=5432/tcp --permanent
sudo firewall-cmd --add-port=9090/tcp --permanent
sudo firewall-cmd --add-port=3000/tcp --permanent
sudo firewall-cmd --reload
```

5) Accès aux services

- Application FastAPI : http://<host>:8000/
- Metrics Prometheus : http://<host>:9090/
- Grafana UI : http://<host>:3000/  (identifiants par défaut si aucun provisionnement)
- PostgreSQL : port 5432 (connexion via psql ou outils graphiques)

6) Commandes utiles récapitulatives

```bash
# Construire et démarrer (arrière-plan)
docker-compose up --build -d
# Voir les logs du service app
docker-compose logs -f app
# Arrêter et nettoyer
docker-compose down
# Lancer localement (venv)
python -m venv .venv && source .venv/bin/activate && pip install -r app/requirements.txt && cd app && uvicorn main:app --reload --port 8000
```

7) Dépannage rapide

- Si l'application ne démarre pas, vérifier `docker-compose logs app` ou `docker logs mspr-app`.
- Vérifiez que PostgreSQL est joignable depuis l'application (host, port, credentials).
- Vérifiez la version de Python si installation locale (utiliser la version 3.9 recommandée par le Dockerfile).

Si vous souhaitez que je :
- exécute les containers pour vous ici, ou
- ajoute un script d'initialisation pour Grafana/Prometheus, ou
- crée des instructions pour déployer sur un serveur (systemd / service), dites-le et je m'en occupe.

