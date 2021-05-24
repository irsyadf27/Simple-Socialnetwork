from datetime import datetime

import pytest


from account.tasks import validate_geolocation_holiday


@pytest.fixture
def abstractapi_geolocation_url():
    return "https://geolocation.url/v1/"


@pytest.fixture
def abstractapi_holiday_url():
    return "https://holidays.url/v1/"


@pytest.fixture
def abstractapi_key():
    return "12345"


@pytest.fixture(autouse=True)
def env_vars(
    monkeypatch,
    abstractapi_key,
):
    monkeypatch.setenv("ABSTRACT_GEO_LOCATION_API_KEY", abstractapi_key)
    monkeypatch.setenv("ABSTRACT_HOLIDAY_API_KEY", abstractapi_key)


@pytest.fixture
def account_id():
    return 1


@pytest.fixture
def registration_ip_address():
    return "180.244.137.211"


@pytest.fixture
def date_joined():
    current_date = datetime.now()
    return [current_date.year, current_date.month, current_date.day]


@pytest.mark.django_db
def test_success(
    requests_mock,
    abstractapi_geolocation_url,
    abstractapi_holiday_url,
    account_id,
    registration_ip_address,
    date_joined,
):

    requests_mock.get(
        f"{abstractapi_geolocation_url}?api_key=AbstractGeoLocationAPIKey.Not.Defined&ip_address=180.244.137.211",
        json={
            "country": "Indonesia",
            "country_code": "ID",
        },
    )

    requests_mock.get(
        "{}?api_key=AbstractHolidayAPIKey.Not.Defined&country=ID&year={}&month={}&day={}".format(
            abstractapi_holiday_url,
            *date_joined,
        ),
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
                "week_day": "Friday",
            }
        ],
    )

    validate_geolocation_holiday(
        account_id, registration_ip_address, date_joined
    )
