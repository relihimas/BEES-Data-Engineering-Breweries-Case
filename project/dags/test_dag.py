from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 0,
}

with DAG(
    dag_id="run_pipeline_tests",
    default_args=default_args,
    catchup=False,
    tags=["tests", "qa"],
) as dag:

    # Assumindo que o código e os testes vivem em /opt/airflow
    test_bronze = BashOperator(
        task_id="test_bronze",
        bash_command="cd /opt/airflow && pytest -q tests/test_bronze_*.py",
    )

    test_silver = BashOperator(
        task_id="test_silver",
        bash_command="cd /opt/airflow && pytest -q tests/test_silver_*.py",
    )

    test_gold = BashOperator(
        task_id="test_gold",
        bash_command="cd /opt/airflow && pytest -q tests/test_gold_*.py",
    )

    test_core = BashOperator(
        task_id="test_core",
        bash_command="cd /opt/airflow && pytest -q tests/test_spark_transformer.py",
    )

    # Execução em sequência (pode alterar para paralelo se quiser)
    test_bronze >> test_silver >> test_gold >> test_core