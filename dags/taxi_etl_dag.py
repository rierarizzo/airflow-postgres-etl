import pandas as pd
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "taxi_data_etl",
    default_args=default_args,
    description="Local ETL for taxi data",
    schedule="@daily",
    start_date=datetime(2026, 6, 15),
    catchup=False,
    tags=["exercise_1"],
) as dag:
    download_task = BashOperator(
        task_id="download_green_taxi_parquet",
        bash_command='curl -o /opt/airflow/green_tripdata_2026-04.parquet "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2026-04.parquet"',
    )

    def clean_taxi_data(input_path, output_path):
        df = pd.read_parquet(input_path)
        filtered_df = df[
            (df["passenger_count"] > 0)
            & (df["fare_amount"] > 0)
            & (df["total_amount"] > 0)
        ]
        filtered_df.to_parquet(output_path, index=False)

    clean_data_task = PythonOperator(
        task_id="clean_data_task",
        python_callable=clean_taxi_data,
        op_kwargs={
            "input_path": "/opt/airflow/green_tripdata_2026-04.parquet",
            "output_path": "/opt/airflow/green_tripdata_2026-04-cleaned.parquet",
        },
    )

    # Task 3: Create table in PostgreSQL
    # create_table_task = SQLExecuteQueryOperator(...)

    # Task 4: Insert data into PostgreSQL
    # insert_data_task = PythonOperator(...) o SQLExecuteQueryOperator(...)

    # Define dependencies (example)
    # download_task >> clean_data_task >> create_table_task >> insert_data_task
    download_task >> clean_data_task
    pass
