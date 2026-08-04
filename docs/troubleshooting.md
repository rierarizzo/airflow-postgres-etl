# Troubleshooting

Common issues and how to resolve them.

## Airflow UI not available

**Symptoms:** `http://localhost:8080` won't load.

**Causes / fixes:**
- **The stack is still initializing.** The `airflow-init` service runs DB migration and admin-user creation before the API server is healthy. Wait a minute, then re-check: `docker compose ps`.
- **Port 8080 is in use.** Change the host port in `compose.yml` (`ports: "8080:8080"`) or stop the conflicting process.
- **Check service health:** `docker compose ps` and `docker compose logs airflow-apiserver`.

## `AIRFLOW_UID` not set

**Symptoms:** `docker compose up` warns about Airflow running as root, or volume permissions break.

**Fix:**

```bash
echo "AIRFLOW_UID=$(id -u)" > .env
docker compose down && docker compose up -d
```

**Note:** `.env` is gitignored, so it must be recreated on a fresh clone.

## Download task fails

**Symptoms:** `download_green_taxi_parquet` errors.

**Causes / fixes:**
- **No network access** to `d37ci6vzurychx.cloudfront.net`. Check connectivity from the container.
- **The monthly file no longer exists.** The URL and output filename are hard-coded to April 2026 in `dags/taxi_etl_dag.py`. Update the month in both the `BashOperator` command and the paths used by the clean/insert tasks to a currently available month.
- **`curl` not present.** The base image `apache/airflow:3.2.2` ships `curl`; if a custom image is used, install it or switch to a downloader operator.

## Port conflicts

**Symptoms:** `port is already allocated` on `5432` (Postgres) or `8080` (Airflow UI).

**Fix:** Stop the process bound to the port, or remap hosts ports in `compose.yml`. The Postgres host port `5432` is the most likely conflict.

## Database connection errors on load tasks

**Symptoms:** `create_table_task` or `insert_data_task` fail with a PostgreSQL connection error.

**Causes / fixes:**
- **The `postgres` service is down.** Check `docker compose ps` and `docker compose logs postgres`.
- **Volume was wiped.** If the Postgres volume was removed, Airflow metadata is also gone; re-run the init flow.

## Data not appearing in the table

**Symptoms:** The DAG succeeds but the table looks empty.

**Checks:**
- Confirm the records matched the filter (`passenger_count > 0`, `fare_amount > 0`, `total_amount > 0`); everything else is dropped by design.
- Connect to the DB and inspect:

```bash
docker compose exec postgres psql -U airflow -d airflow \
  -c 'SELECT COUNT(*) FROM green_tripdata;'
```

**Note:** Query quoted columns like `"PULocationID"` with double quotes (see [Database Schema](database-schema.md)).