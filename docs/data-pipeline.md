# Data Pipeline (ETL)

This page describes the end-to-end Extract, Transform, Load flow implemented by the DAG.

```
Extract ──► Transform ──► Create Table (infra) ──► Load ──► PostgreSQL
```

## 1. Extract

The pipeline downloads **NYC Green Taxi** trip records from the official NYC TLC public source:

```
https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2026-04.parquet
```

- **Format:** Parquet
- **Source month:** April 2026
- **Destination:** `/opt/airflow/green_tripdata_2026-04.parquet` (inside the Airflow container)

This month is hard-coded in the `BashOperator` command, so the file must be updated periodically to keep pulling new data.

## 2. Transform

The `clean_taxi_data` function applies data-quality rules using Pandas.

### Filtering Rules (as-built)

Records are kept only when **all** of the following are true:

- `passenger_count > 0`
- `fare_amount > 0`
- `total_amount > 0`

```python
filtered_df = df[
    (df["passenger_count"] > 0)
    & (df["fare_amount"] > 0)
    & (df["total_amount"] > 0)
]
```

The resulting DataFrame is written to `/opt/airflow/green_tripdata_2026-04-cleaned.parquet`.

### Note on the task spec

The repo's `INSTRUCTIONS.md` asks to drop rows with **null** values in `total_amount` and `fare_amount`. The code instead filters on **value greater than zero**. The implementation achieves a similar goal (removing missing/invalid billing records) but is not byte-for-byte what the spec describes. The docs reflect the **as-built** behavior in `dags/taxi_etl_dag.py`.

## 3. Infrastructure (Create Table)

The `create_table_task` runs `CREATE TABLE IF NOT EXISTS green_tripdata (...)` against the `postgres_local` connection, guaranteeing the destination table exists before any insert. See [Database Schema](database-schema.md) for the full column list.

## 4. Load

The `insert_data` function appends the cleaned records:

```python
df.to_sql(
    "green_tripdata",
    engine,
    if_exists="append",   # add rows, never overwrite
    index=False,
    chunksize=1000,
    method="multi",       # multi-row inserts
)
```

- `if_exists="append"` ensures data is **added**, not truncated.
- `chunksize=1000` and `method="multi"` batch inserts for efficiency.

## Data Flow Summary

| Stage   | Input                                          | Output                                    |
|---------|------------------------------------------------|-------------------------------------------|
| Extract | NYC TLC Parquet URL                            | Raw Parquet file                          |
| Transform | Raw Parquet file                            | Cleaned Parquet file                      |
| Load    | Cleaned Parquet file                           | Rows in `green_tripdata` table            |