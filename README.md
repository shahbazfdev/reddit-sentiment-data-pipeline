# Reddit Sentiment & Analytics Data Pipeline

An end-to-end **production-grade data engineering pipeline** orchestrated with **Apache Airflow (Astronomer Runtime)** to ingest data from Reddit, enrich it using Natural Language Processing (sentiment analysis & intent classification), load it into PostgreSQL, and model it using dimensional modeling (Star Schema) principles.

---

## Architecture Overview

```
Reddit API (PRAW)
       │
       ▼
 [1. Raw JSON Extraction]  ──► /usr/local/airflow/data/reddit/raw/
       │
       ▼
 [2. Refined CSV Transformation & NLP] ──► Sentiment Analysis & Intent Heuristics
       │
       ▼
 [3. PostgreSQL Staging Load] ──► stg_reddit_posts
       │
       ▼
 [4. Incremental Merge / Deduplication] ──► reddit_posts (Unique Records)
       │
       ▼
 [5. Dimensional Modeling (Star Schema)] ──► fact_reddit_posts & dim_* tables
       │
       ▼
 [6. Housekeeping & Cleanup] ──► Automated retention & staging truncation
```

### Tech Stack & Components
- **Orchestration**: Apache Airflow 3 / Astronomer Runtime (`astro-runtime:3.1-8`)
- **Container Runtime**: Docker (Docker Engine or docker-podman wrapper)
- **Data Ingestion**: Python Reddit API Wrapper (`praw`)
- **Data Transformation & NLP**: Pandas, `vaderSentiment`, custom NLP intent classification
- **Storage & Data Warehouse**: PostgreSQL 15 (Staging, Normalized Store, & Star Schema)
- **Data Modeling**: SQL-based dimensional modeling (Kimball methodology)

---

## Prerequisites & Docker Setup

### 1. Docker Runtime Setup

Ensure Docker (or the docker-podman wrapper socket) is running on your machine:

```bash
systemctl --user enable --now podman.socket
export DOCKER_HOST=unix:///run/user/$UID/podman/podman.sock
docker ps
```
*(Tip: Add `export DOCKER_HOST=unix:///run/user/$UID/podman/podman.sock` to your `~/.bashrc` or `~/.zshrc`)*.

---

### 2. Install Astro CLI

The Astronomer CLI (`astro`) makes spinning up and managing the entire containerized Airflow stack effortless.

#### Linux / macOS:
```bash
curl -sSL install.astronomer.io | bash -s -- --install-dir ~/.local/bin
```
*(Ensure `~/.local/bin` is in your `$PATH`)*.

#### Windows (PowerShell):
```powershell
winget install -e --id Astronomer.Astro
```

Verify installation:
```bash
astro version
```

---

## Quick Start & Running the Project

### 1. Clone and Navigate to Project
```bash
git clone https://github.com/shahbazfdev/reddit-sentiment-data-pipeline.git
cd reddit-sentiment-data-pipeline
```

### 2. Start Airflow with Containers
From the project root:
```bash
astro dev start
```
*Alternatively, if managing via Docker directly:*
```bash
docker start $(docker ps -a -q --filter name=airflow-dev)
```

This starts:
- **Airflow Web UI / API Server**: `http://localhost:8080` (Default credentials: `admin` / `admin`)
- **Airflow Scheduler & Triggerer**
- **Airflow DAG Processor**
- **PostgreSQL 15 Container**: `localhost:5432`

---

## Configuration (Connections & Variables)

### 1. Reddit API Connection
Obtain your API credentials by creating an application of type **script** at [Reddit App Preferences](https://www.reddit.com/prefs/apps).

In **Airflow UI → Admin → Connections → Add Connection**:
- **Connection Id**: `reddit_api`
- **Connection Type**: `Generic`
- **Login**: `<Your Reddit Client ID>`
- **Password**: `<Your Reddit Client Secret>`
- **Extra (JSON)**:
```json
{
  "user_agent": "python:DataAnalyzer:1.0 (by /u/YOUR_REDDIT_USERNAME)"
}
```

### 2. Dynamic Reddit Config Variable
In **Airflow UI → Admin → Variables → Add Variable**:
- **Key**: `reddit_config`
- **Value (JSON)**:
```json
{
  "subreddits": ["technology", "programming", "python", "dataengineering"],
  "post_type": "new",
  "limit": 100
}
```

### 3. Target PostgreSQL Warehouse Setup
Create the analytical database inside the Postgres container:
```bash
docker exec airflow-dev_e1fe2a-postgres-1 psql -U postgres -c "CREATE DATABASE af_reddit;"
```

In **Airflow UI → Admin → Connections → Add Connection**:
- **Connection Id**: `postgres_reddit`
- **Connection Type**: `Postgres`
- **Host**: `postgres` *(container DNS alias on the docker network)*
- **Database / Schema**: `af_reddit`
- **Login**: `postgres`
- **Password**: `postgres`
- **Port**: `5432`

---

## Pipeline DAGs Overview

Execute the DAGs in the following order:

| Step | DAG ID | Description |
|---|---|---|
| **1** | `reddit_extract_dag` | Ingests posts via PRAW and stores raw JSON files into `/usr/local/airflow/data/reddit/raw/` |
| **2** | `reddit_transform_dag` | Processes raw JSON, computes sentiment scores and intent metrics, and outputs clean CSVs |
| **3** | `reddit_load_dag` | Copies refined CSV records into the staging table `stg_reddit_posts` |
| **4** | `reddit_incremental_load_dag` | Performs deduplication and merges newly arrived posts into `reddit_posts` |
| **5** | `reddit_dimensional_model_dag` | Transforms staged data into analytical Star Schema tables (`fact_*` and `dim_*`) |
| **6** | `reddit_cleanup_dag` *(Adhoc)* | Truncates staging tables and purges older processed raw/refined files |

---

## Data Warehouse & Dimensional Model

### Tables
1. **`stg_reddit_posts`**: Transient staging table capturing incoming CSV records with initial validations.
2. **`reddit_posts`**: Intermediate deduplicated store retaining unique Reddit submissions by natural key (`id`).
3. **`fact_reddit_posts`**: Core fact table with measurable post metrics (upvotes, ratio, comment counts, sentiment score, extraction timestamp).
4. **`dim_author`**: Dimension table storing unique Reddit user details.
5. **`dim_subreddit`**: Dimension table storing subreddit metadata.
6. **`dim_raw_source_file`**: Audit dimension tracking lineage back to original raw JSON files.
7. **`dim_refined_source_file`**: Lineage dimension tracking intermediate processed CSV files.

---

## Handy Docker Commands

```bash
# Check running containers
docker ps

# Follow Airflow scheduler logs
docker logs -f airflow-dev_e1fe2a-scheduler-1

# Stop all Airflow pipeline containers
docker stop $(docker ps -q --filter name=airflow-dev)

# Start all Airflow pipeline containers
docker start $(docker ps -a -q --filter name=airflow-dev)

# Query the analytical database
docker exec -it airflow-dev_e1fe2a-postgres-1 psql -U postgres -d af_reddit
```

---

## Author

**Shahbaz Fareed Chishti**  
- **Email**: [shahbazfdev@gmail.com](mailto:shahbazfdev@gmail.com)  
- **GitHub**: [@shahbazfdev](https://github.com/shahbazfdev)  
- **Role**: Data Engineer  
- **Focus**: Data Engineering, Cloud Infrastructure, Distributed Systems & Analytical Pipelines
