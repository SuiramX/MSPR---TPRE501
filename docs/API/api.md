# Documentation de l'API

L'API HealthAI Coach est une API REST développée avec **FastAPI**. Elle expose les données de santé et de fitness stockées en base PostgreSQL.

- **URL locale** : `http://localhost:8000`
- **Documentation interactive (Swagger)** : `http://localhost:8000/docs`

---

## Authentification

Les routes **POST**, **PUT**, **DELETE** et les exports CSV nécessitent une clé d'API.

Elle doit être transmise dans le header HTTP suivant :

```
X-API-Key: healthai_key
```

Les routes **GET** sont publiques et ne nécessitent pas d'authentification.

---

## Endpoints

### Members `/members`

| Méthode | Route | Description | Auth |
|---|---|---|---|
| GET | `/members` | Liste des membres (pagination : `skip`, `limit`) | Non |
| GET | `/members/{id}` | Détail d'un membre | Non |
| POST | `/members` | Créer un membre | Oui |
| PUT | `/members/{id}` | Modifier un membre | Oui |
| DELETE | `/members/{id}` | Supprimer un membre | Oui |

---

### Foods `/foods`

| Méthode | Route | Description | Auth |
|---|---|---|---|
| GET | `/foods` | Liste des aliments | Non |
| GET | `/foods/{id}` | Détail d'un aliment | Non |
| POST | `/foods` | Créer un aliment | Oui |
| PUT | `/foods/{id}` | Modifier un aliment | Oui |
| DELETE | `/foods/{id}` | Supprimer un aliment | Oui |

---

### Exercises `/exercises`

| Méthode | Route | Description | Auth |
|---|---|---|---|
| GET | `/exercises` | Liste des exercices | Non |
| GET | `/exercises/{id}` | Détail d'un exercice | Non |
| POST | `/exercises` | Créer un exercice | Oui |
| PUT | `/exercises/{id}` | Modifier un exercice | Oui |
| DELETE | `/exercises/{id}` | Supprimer un exercice | Oui |

---

### Workouts `/workouts`

| Méthode | Route | Description | Auth |
|---|---|---|---|
| GET | `/workouts/{id}` | Détail d'une séance | Non |
| GET | `/workouts/member/{member_id}` | Séances d'un membre | Non |
| POST | `/workouts` | Créer une séance | Oui |
| PUT | `/workouts/{id}` | Modifier une séance | Oui |
| DELETE | `/workouts/{id}` | Supprimer une séance | Oui |

---

### Plans `/plans`

| Méthode | Route | Description | Auth |
|---|---|---|---|
| GET | `/plans` | Liste des plans | Non |
| GET | `/plans/{id}` | Détail d'un plan | Non |
| POST | `/plans` | Créer un plan | Oui |
| PUT | `/plans/{id}` | Modifier un plan | Oui |
| DELETE | `/plans/{id}` | Supprimer un plan | Oui |

---

### Export CSV `/export`

Toutes les routes d'export nécessitent l'API Key. Elles retournent un fichier `.csv` en téléchargement.

| Méthode | Route | Fichier retourné |
|---|---|---|
| GET | `/export/members/csv` | `members.csv` |
| GET | `/export/foods/csv` | `foods.csv` |
| GET | `/export/exercises/csv` | `exercises.csv` |
| GET | `/export/workouts/csv` | `workouts.csv` |
| GET | `/export/plans/csv` | `plans.csv` |
