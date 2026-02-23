from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from app.bronze.service import BronzeService
from app.silver.service import SilverService
from app.gold.service import GoldService

def bronze_task():
    BronzeService().run()

def silver_task():
    SilverService().run()

def gold_task():
    GoldService().run()

with DAG(
    dag_id="breweries_full_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    bronze = PythonOperator(
        task_id="bronze",
        python_callable=bronze_task
    )

    silver = PythonOperator(
        task_id="silver",
        python_callable=silver_task
    )

    gold = PythonOperator(
        task_id="gold",
        python_callable=gold_task
    )

    bronze >> silver >> gold