from app.bronze.service import BronzeService
from app.bronze.http_client import BreweryApiClient
from app.bronze.repository import BronzeRepository


def run_bronze():
    service = BronzeService(
        api_client=BreweryApiClient(),
        repository=BronzeRepository(),
    )
    service.run()


if __name__ == "__main__":
    run_bronze()