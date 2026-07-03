## 🏗️ DataFlow-Platform — Projet 2

**Idée fil rouge :** Plateforme de données e-commerce qui ingère des commandes en temps réel et en batch, les traite avec Spark, et les expose dans un Lakehouse.

---

### Architecture complète :

```
Sources de données
├── API commandes (batch)      ──► Airflow ──► S3 Bronze
├── Kafka (commandes temps réel) ──► Spark Streaming ──► S3 Bronze
└── PostgreSQL (clients/produits) ──► Airbyte ──► S3 Bronze
                                              ▼
                                    Apache Spark (PySpark)
                                    Nettoyage + validation
                                              ▼
                                         S3 Silver
                                    (Delta Lake format)
                                              ▼
                                    dbt transformations
                                    marts analytiques
                                              ▼
                                         S3 Gold
                                    (Redshift / BigQuery)
                                              ▼
                                    Dashboard Streamlit
```

---

### Phases du projet :

## Phase 0 — Fondations
- PostgreSQL local avec données e-commerce (clients, commandes, produits)
- Script Python pour générer des données réalistes avec Faker
- Modèles Pydantic V2 pour valider les données
- Tests pytest + CI/CD GitHub Actions

**Phase 1 — Ingestion Batch avec Airbyte **
- Installer Airbyte via Docker
- Connecter PostgreSQL → S3 (Bronze layer)
- Comprendre les connecteurs no-code/low-code
- Planifier les syncs dans Airflow

**Phase 2 — Traitement PySpark (Actuellement à cette phase)**
- Installer Spark local via Docker
- Lire les fichiers Parquet depuis S3
- Transformations Spark : nettoyage, agrégations, joins
- Écrire en format Delta Lake (Silver layer)
- Tests unitaires PySpark

**Phase 3 — Streaming Kafka **
- Kafka via Docker Compose
- Producer Python : simule des commandes en temps réel
- Consumer PySpark Streaming : traitement en micro-batch
- Écriture dans S3 Bronze en temps réel

**Phase 4 — AWS Cloud **
- S3 pour le stockage (Bronze/Silver/Gold)
- AWS Glue pour le catalogue de données
- Redshift comme Data Warehouse
- IAM : gestion des permissions

**Phase 5 — Infrastructure as Code **
- Terraform pour provisionner S3, Redshift, IAM
- Versionner l'infrastructure sur GitHub
- Déployer avec `terraform apply`

**Phase 6 — Architecture Medallion complète **
- Bronze : données brutes
- Silver : données nettoyées (Spark)
- Gold : marts analytiques (dbt)
- Documentation du lineage

**Phase 7 — Orchestration avancée **
- DAG Airflow complet (batch + streaming)
- Alertes par email en cas d'échec
- SLA monitoring
- Backfill des données historiques

**Phase 8 — Kubernetes **
- Déployer Airflow sur Kubernetes (KubernetesExecutor)
- Déployer Spark sur Kubernetes
- Helm charts
- Scaling automatique

---

### Stack complète :

```
Langage     : Python 3.12 + PySpark
Ingestion   : Airbyte (no-code) + connecteurs Python custom
Streaming   : Apache Kafka + Spark Streaming
Traitement  : Apache Spark (PySpark)
Stockage    : AWS S3 + Delta Lake
Warehouse   : Amazon Redshift + dbt-core
Orchestration: Apache Airflow
Infrastructure: Terraform + Kubernetes
Base de données: PostgreSQL + MongoDB
CI/CD       : GitHub Actions + Docker
Qualité     : pytest + Great Expectations
Visualisation: Streamlit
```