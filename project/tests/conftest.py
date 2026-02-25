import pytest
from app.bronze.schemas import Brewery

@pytest.fixture
def sample_brewery_list():
    return [
        Brewery(
            id="1",
            name="Test Brewery",
            brewery_type="micro",
            address_1="Street 1",
            address_2=None,
            address_3=None,
            city="Recife",
            state_province=None,
            postal_code="50000-000",
            country="Brazil",
            longitude="-34.9",
            latitude="-8.0",
            phone="81999999999",
            website_url="http://test.com",
            state="PE",
            street="Street 1",
        )
    ]