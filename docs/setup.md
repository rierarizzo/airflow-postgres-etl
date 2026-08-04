# Setup & First Run

This guide covers installing and running the ETL pipeline on a local machine.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) with [Docker Compose v2](https://docs.docker.com/compose/)
- A Unix-like shell (for `id -u` in the preflight step)

## Preflight Steps

Create the folders that Airflow mounts as volumes:

```bash
mkdir -p ./dags ./logs ./plugins
```

Create a `.env` file containing the numeric UID Airflow should run as:

```bash
echo "AIRFLOW_UID=$(id -u)" > .env
```

> **Note:** `.env` and `logs/` are gitignored — they are local-only. Duplicate raw data files live under `datasets/`, which is also gitignored.

## Starting the Stack

```bash
docker compose up -d
```

This starts the following services (defined in `compose.yml`):

- `postgres` — PostgreSQL 15 database
- `airflow-init` — runs DB migration and creates the `admin` user (one-off)
- `airflow-apiserver` — Airflow UI/API on port `8080`
- `airflow-scheduler` — schedules and dispatches DAG runs
- `airflow-dag-processor` — parses DAG files
- `airflow-triggerer` — supports deferrable tasks

> **First run may take a minute.** The `airflow-init` service must complete before the UI becomes available.

### Access the UI

Open **http://localhost:8080**.

Credentials: **admin** / **admin**

The DAG `taxi_data_etl` is created paused (`DAGS_ARE_PAUSED_AT_CREATION=true`). Unpause it to start the daily schedule, or trigger it manually.

## Stopping the Stack

```bash
docker compose down
```

## Full Teardown (Remove Data)

Stop everything and delete the PostgreSQL volume:

```bash
docker compose down -v
```

> This permanently removes the Airflow metadata database and any loaded trip data. Use with care.

## Verifying It Works

1. Open the Airflow UI and confirm the `taxi_data_etl` DAG appears in the **DAGs** list.
2. Unpause and trigger a run, then watch the four tasks execute in sequence.
3. Check the data landed in the `green_tripdata` table (see [Database Schema](database-schema.md)).

If something fails, see [Troubleshooting](troubleshooting.md).