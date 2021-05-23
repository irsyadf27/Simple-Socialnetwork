from http import HTTPStatus

import pytest
from datetime import datetime
from account.tasks import validate_geolocation_holiday
from account.models import Account


@pytest.fixture
def geolocation_url():
    return "https://geolocation.url"


@pytest.fixture
def holiday_url():
    return "https://holiday.url"


@pytest.fixture
def abstractapi_key():
    return "12345"


@pytest.fixture(autouse=True)
def env_vars(
    monkeypatch, abstractapi_key
):
    monkeypatch.setenv("ABSTRACT_API_KEY", abstractapi_key)


@pytest.fixture
def account_id():
    return 1


@pytest.fixture
def registration_ip_address():
    return "180.244.137.211"


@pytest.fixture
def date_joined():
    return datetime.now()


def test_success(
    requests_mock, geolocation_url, holiday_url, account_id, registration_ip_address, date_joined
):
    requests_mock.get(
        f"{geolocation_url}/v1/?api_key=12345&ip_address=180.244.137.211",
        json={
            "country": "Indonesia",
            "country_code": "ID",
        },
    )

    requests_mock.get(
        f"{holiday_url}/v1/?api_key=12345&country=ID&year=2020&month=12&day=25",
        json=[
            {
                "name": "Christmas Day",
                "name_local": "",
                "language": "",
                "description": "",
                "country": "ID",
                "location": "Indonesia",
                "type": "National",
                "date": "12/25/2020",
                "date_year": "2020",
                "date_month": "12",
                "date_day": "25",
                "week_day": "Friday"
            }
        ],
    )

    validate_geolocation_holiday(
        account_id, registration_ip_address, date_joined
    )