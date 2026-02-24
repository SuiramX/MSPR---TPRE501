# 5. API REST documentée

## Vue d'ensemble

L'API REST HealthAI Coach est développée avec **FastAPI** et expose les données de la plateforme stockées dans **PostgreSQL**. Elle tourne sur le port `8000` et génère automatiquement une documentation interactive disponible sur `/docs` (Swagger UI).

**Stack technique :**

| Composant | Technologie |
|---|---|
| Framework API | FastAPI + Uvicorn |
| ORM | SQLAlchemy |
| Base de données | PostgreSQL 15 |
| Validation des données | Pydantic v2 |
| Export CSV | Pandas |
| Monitoring | Prometheus + Grafana |
| Containerisation | Docker / Docker Compose |

---

## Accès à l'API

L'API est accessible sur : `http://localhost:8000`
La documentation Swagger est accessible sur : `http://localhost:8000/docs`

## Sécurité

Les routes de **lecture** (GET) sont **publiques**.
Les routes d'**écriture** (POST, PUT, DELETE) et d'**export CSV** sont **protégées par une API Key**.

**Header à fournir pour les routes protégées :**

```
X-API-Key: healthai_key
```

En cas de clé invalide ou absente → réponse `403 Forbidden`.

---

## Endpoints

### Members — `/members`

Profils utilisateurs (âge, genre, poids, taille, IMC, % de graisse corporelle).

| Méthode | Route | Auth | Description |
|---|---|---|---|
| GET | `/members/` | Non | Liste des membres (pagination `skip`/`limit`) |
| GET | `/members/{id}` | Non | Détail d'un membre |
| POST | `/members/` | Oui | Créer un membre |
| PUT | `/members/{id}` | Oui | Modifier un membre |
| DELETE | `/members/{id}` | Oui | Supprimer un membre |

---

### Foods — `/foods`

Base nutritionnelle : aliments avec leurs valeurs nutritionnelles (calories, protéines, glucides, lipides, fibres, sodium, sucre).

| Méthode | Route | Auth | Description |
|---|---|---|---|
| GET | `/foods/` | Non | Liste des aliments |
| GET | `/foods/{id}` | Non | Détail d'un aliment |
| POST | `/foods/` | Oui | Créer un aliment |
| PUT | `/foods/{id}` | Oui | Modifier un aliment |
| DELETE | `/foods/{id}` | Oui | Supprimer un aliment |

---

### Exercises — `/exercises`

Catalogue d'exercices sportifs (type, groupe musculaire, équipement requis, niveau de difficulté, instructions).

> La clé primaire est une chaîne de caractères (`id_exercise`), pas un entier.
> La création vérifie l'unicité de l'id → `409 Conflict` si l'exercice existe déjà.

| Méthode | Route | Auth | Description |
|---|---|---|---|
| GET | `/exercises/` | Non | Liste des exercices |
| GET | `/exercises/{id}` | Non | Détail d'un exercice |
| POST | `/exercises/` | Oui | Créer un exercice |
| PUT | `/exercises/{id}` | Oui | Modifier un exercice |
| DELETE | `/exercises/{id}` | Oui | Supprimer un exercice |

---

### Workouts — `/workouts`

Sessions d'entraînement liées aux membres (type, durée, calories brûlées, fréquence, niveau d'expérience).

| Méthode | Route | Auth | Description |
|---|---|---|---|
| GET | `/workouts/` | Non | Liste des sessions |
| GET | `/workouts/{id}` | Non | Détail d'une session |
| GET | `/workouts/member/{member_id}` | Non | Toutes les sessions d'un membre |
| POST | `/workouts/` | Oui | Créer une session (vérifie que le membre existe) |
| PUT | `/workouts/{id}` | Oui | Modifier une session |
| DELETE | `/workouts/{id}` | Oui | Supprimer une session |

---

### Plans — `/plans`

Plans personnalisés de santé (objectif, catégorie IMC, programme sportif et alimentaire recommandé).

| Méthode | Route | Auth | Description |
|---|---|---|---|
| GET | `/plans/` | Non | Liste des plans |
| GET | `/plans/{id}` | Non | Détail d'un plan |
| POST | `/plans/` | Oui | Créer un plan |
| PUT | `/plans/{id}` | Oui | Modifier un plan |
| DELETE | `/plans/{id}` | Oui | Supprimer un plan |

---

### Export CSV — `/export`

Export des données nettoyées au format CSV. Les colonnes techniques (`source_file`, `ingested_at`) sont exclues de l'export.

| Méthode | Route | Auth | Fichier généré |
|---|---|---|---|
| GET | `/export/members/csv` | Oui | `members.csv` |
| GET | `/export/foods/csv` | Oui | `foods.csv` |
| GET | `/export/exercises/csv` | Oui | `exercises.csv` |
| GET | `/export/workouts/csv` | Oui | `workouts.csv` |
| GET | `/export/plans/csv` | Oui | `plans.csv` |

---

### Monitoring — Endpoints système

| Route | Auth | Description |
|---|---|---|
| `GET /` | Non | Vérifie que l'API est en ligne |
| `GET /metrics` | Non | Métriques Prometheus |
| `GET /docs` | Non | Documentation Swagger interactive |
| `GET /redoc` | Non | Documentation ReDoc |