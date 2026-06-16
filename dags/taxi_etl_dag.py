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
    # Tarea 1: Descargar archivo
    # download_task = BashOperator(...)

    # Tarea 2: Limpiar datos con Pandas
    # clean_data_task = PythonOperator(...)

    # Tarea 3: Crear tabla en PostgreSQL
    # create_table_task = SQLExecuteQueryOperator(...)

    # Tarea 4: Insertar datos en PostgreSQL
    # insert_data_task = PythonOperator(...) o SQLExecuteQueryOperator(...)

    # Definir dependencias (ejemplo)
    # download_task >> clean_data_task >> create_table_task >> insert_data_task
    pass