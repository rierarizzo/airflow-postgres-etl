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
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    "taxi_data_etl",
    default_args=default_args,
    description="Local ETL for taxi data",
    schedule_interval="@daily",
    start_date=datetime(2026, 6, 15),
    catchup=False,
    tags=["exercise_1"],
) as dag:
    # Task 1: Download file
    # download_task = BashOperator(...)

    # Task 2: Clean data with Pandas
    # clean_data_task = PythonOperator(...)

    # Task 3: Create table in PostgreSQL
    # create_table_task = SQLExecuteQueryOperator(...)

    # Task 4: Insert data into PostgreSQL
    # insert_data_task = PythonOperator(...) o SQLExecuteQueryOperator(...)

    # Define dependencies (example)
    # download_task >> clean_data_task >> create_table_task >> insert_data_task
    pass