# Database Schema

The destination table is created by `sql/create_table__green_tripdata.sql` via the `create_table_task`. It mirrors the structure of the processed Parquet file.

## Table: `green_tripdata`

Created with `CREATE TABLE IF NOT EXISTS`, so it is safe to re-run.

| Column                | Type                              | Quoted       |
|-----------------------|-----------------------------------|--------------|
| `VendorID`            | INTEGER                           | Yes (`"..."`)|
| `lpep_pickup_datetime`| TIMESTAMP WITHOUT TIME ZONE      | No           |
| `lpep_dropoff_datetime`| TIMESTAMP WITHOUT TIME ZONE     | No           |
| `store_and_fwd_flag`  | TEXT                              | No           |
| `RatecodeID`          | FLOAT(53)                         | Yes (`"..."`)|
| `PULocationID`        | INTEGER                           | Yes (`"..."`)|
| `DOLocationID`        | INTEGER                           | Yes (`"..."`)|
| `passenger_count`     | FLOAT(53)                         | No           |
| `trip_distance`       | FLOAT(53)                         | No           |
| `fare_amount`         | FLOAT(53)                         | No           |
| `extra`               | FLOAT(53)                         | No           |
| `mta_tax`             | FLOAT(53)                         | No           |
| `tip_amount`          | FLOAT(53)                         | No           |
| `tolls_amount`        | FLOAT(53)                         | No           |
| `ehail_fee`           | FLOAT(53)                         | No           |
| `improvement_surcharge`| FLOAT(53)                        | No           |
| `total_amount`        | FLOAT(53)                         | No           |
| `payment_type`        | FLOAT(53)                         | No           |
| `trip_type`           | FLOAT(53)                         | No           |
| `congestion_surcharge`| FLOAT(53)                         | No           |
| `cbd_congestion_fee`  | FLOAT(53)                         | No           |

## Notes

- Columns `VendorID`, `RatecodeID`, `PULocationID`, and `DOLocationID` are defined with double-quoted identifiers in the DDL. This preserves the exact capitalization used by the Parquet source. These columns must be referenced with quotes in queries, e.g. `SELECT "PULocationID" FROM green_tripdata;`.
- Monetary/fare columns use `FLOAT(53)` (double precision), matching the Parquet schema.
- There are no primary keys or constraints — the table is a direct append target for the ETL load.