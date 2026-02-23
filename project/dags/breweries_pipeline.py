from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from app.bronze.service import BronzeService
from app.silver.service import SilverService
from app.gold.service import GoldService
from app.bronze.http_client import BreweryApiClient
from app.bronze.repository import BronzeRepository

def bronze_task():
    BronzeService(
        api_client=BreweryApiClient(),
        repository=BronzeRepository(),
    ).run()

def silver_task():
    SilverService().run()

def gold_task():
    GoldService().run()

with DAG(
    dag_id="breweries_full_pipeline",
    start_date=datetime(2025, 1, 1),
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