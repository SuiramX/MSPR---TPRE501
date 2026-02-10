Pipeline ETL (extract, transform, load)

## Objectifs :


Extraire des datas

Transformer les datas pour notre usage

Téléversers les datas dans la base de donnée

Monitorer toutes les transactions 


---
## Extraire


- Volume des CSV (taille, fréquence de mise à jour)
- Schéma stable ou évolutif ?
- JSON GitHub :  public / privé  polling / webhook
- API :  auth (token, OAuth, clé)   rate limit  pagination  

### Points de réflexion


- Conditionne la stratégie d’ingestion
- Détermine la charge, la latence et la robustesse nécessaires
- CSV volumineux → ingestion batch, découpage, COPY PostgreSQL
- Schéma instable → zone *raw* + transformations différées
- GitHub polling → jobs planifiés  
- GitHub webhook → ingestion événementielle
- API avec rate limit → backoff, cache, incrémental

### Nos Choix


---
# Transformer


Où se fait la transformation ?  
  - scripts Python existants  
  - dans FastAPI  
  - job dédié
- Transformations lourdes ou légères ?
- Validation / contrôle qualité des données requis ?


### Points de réflexion
- Définit le mode de déclenchement et la reproductibilité


- Batch planifié → simple, prédictible
- Événementiel → plus réactif, plus complexe
- Conservation des données brutes → audit, rollback, coût disque

### Nos Choix

----
# Televerser

- Modèle PostgreSQL :  
  - tables normalisées  
  - tables de faits / dimensions  
- Upsert, overwrite, append ?
- Gestion des doublons ?

### Points de réflexion
Impact direct sur la maintenabilité et les performances
- Scripts Python isolés → clarté, testabilité
- Transformation dans FastAPI → couplage fort
- Transformations lourdes → conteneur dédié, parallélisation
- Validation des données → détection d’erreurs précoces

### Nos Choix


---

 # Monitoring
 
- Ce que tu veux mesurer avec Prometheus :  
  - durée des jobs  
  - taux d’erreur  
  - volumétrie  
- Alerting requis ?  
  - seuils  
  - notifications (mail, webhook)

### Points de réflexion
**Permet de savoir *si* et *quand* ça casse**

- Métriques minimales → visibilité faible
- Métriques fines → diagnostic rapide
- Alertes → réactivité
- Sans alertes → dépendance à Grafana

### Nos Choix
---


# Conteneurisation
2 options :
Docker Compose VS Conteneurs séparés 

## Docker Compose

### Usage
- Scripts ETL
- Base PostgreSQL
- Prometheus
- Grafana

### Avantages
- Déploiement atomique
- Réseau interne automatique
- Versionnable (git)
- Reproductibilité totale

### Limites
- Couplage fort
- Scalabilité limitée
- Pas adapté au multi-host

---

## Conteneur séparés

### Usage
- PostgreSQL externe
- Prometheus partagé
- Grafana partagé
- ETL comme job isolé

### Avantages
- Scalabilité
- Séparation des responsabilités
- Migration vers Kubernetes facilitée

### Limites
- Configuration réseau explicite
- Plus de glue (auth, endpoints)

---
# Gestion des secrets

- Gestion des secrets (DB, API) ?
- Accès Grafana restreint ?

### Nos Choix