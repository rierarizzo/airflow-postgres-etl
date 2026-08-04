# DAG Reference

This page documents the `taxi_data_etl` DAG defined in `dags/taxi_etl_dag.py`.

## DAG Configuration

| Attribute       | Value                                          | Notes                                  |
|-----------------|------------------------------------------------|----------------------------------------|
| `dag_id`        | `taxi_data_etl`                                |                                        |
| `schedule`      | `@daily`                                       | Runs once per day                      |
| `start_date`    | `2026-06-15`                                   | DAG history base date                  |
| `catchup`       | `False`                                        | No backfilling on scheduling           |
| `retries`       | `1`                                            | One retry on failure                   |
| `retry_delay`   | `5 minutes`                                    | Wait between retries                   |
| `template_searchpath` | `/opt/airflow/sql`                      | SQL files are resolved from this path  |

Default args apply to every task: `owner=airflow`, no email on failure/retry.

## Tasks

| Task ID                | Operator             | Purpose                                        |
|------------------------|----------------------|------------------------------------------------|
| `download_green_taxi_parquet` | `BashOperator` | Downloads the Green Taxi Parquet file          |
| `clean_data_task`      | `PythonOperator`     | Filters the dataset with Pandas                |
| `create_table_task`    | `SQLExecuteQueryOperator` | Ensures the destination table exists    |
| `insert_data_task`     | `PythonOperator`     | Loads cleaned data into PostgreSQL             |

### Execution Order

```
download_green_taxi_parquet
        │
        ▼
clean_data_task
        │
        ▼
create_table_task
        │
        ▼
insert_data_task
```

### 1. download_green_taxi_parquet

A `BashOperator` that runs `curl` to fetch the source Parquet file:

```bash
curl -o /opt/airflow/green_tripdata_2026-04.parquet \
  "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2026-04.parquet"
```

Output is written to the Airflow working directory so downstream tasks can consume it.

### 2. clean_data_task

A `PythonOperator` calling `clean_taxi_data(input_path, output_path)`:

- Reads the source Parquet with `pd.read_parquet`.
- Keeps only rows where `passenger_count > 0`, `fare_amount > 0`, and `total_amount > 0`.
- Writes the result to `/opt/airflow/green_tripdata_2026-04-cleaned.parquet`.

### 3. create_table_task

A `SQLExecuteQueryOperator` using `conn_id="postgres_local"` that runs `create_table__green_tripdata.sql`. It applies a `CREATE TABLE IF NOT EXISTS` so the table exists regardless of the current state.

### 4. insert_data_task

A `PythonOperator` calling `insert_data(input_path, conn_id)`:

- Reads the cleaned Parquet.
- Uses `PostgresHook.get_sqlalchemy_engine()`.
- Calls `df.to_sql(..., if_exists="append", chunksize=1000, method="multi")` to append rows.

## Airflow Connection

The DAG relies on a connection ID `postgres_local`, defined in `compose.yml`:

```
AIRFLOW_CONN_POSTGRES_LOCAL: "postgresql://airflow:airflow@postgres:5432/airflow"
```