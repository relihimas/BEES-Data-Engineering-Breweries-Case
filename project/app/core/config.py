from pydantic_settings import BaseSettings
from pydantic import AnyUrl, Field


class Settings(BaseSettings):
    # Database
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "airflow"
    postgres_user: str = "airflow"
    postgres_password: str = "airflow"
    postgres_conn_id: str = "postgres_conn"
    postgres_url: str = "jdbc:postgresql://postgres:5432/airflow"

    # API
    metadata_url: str = "https://api.openbrewerydb.org/v1/breweries/meta"
    breweries_url: str = "https://api.openbrewerydb.org/v1/breweries"

    # Bronze tables
    bronze_table: str = "bronze_breweries"
    bronze_simulation_table: str = "bronze_breweries_simulation"

    # Silver tables
    silver_table: str = "silver_breweries"

    # Gold tables
    gold_table: str = "gold_breweries"

    class Config:
        env_file = ".env"

settings = Settings()