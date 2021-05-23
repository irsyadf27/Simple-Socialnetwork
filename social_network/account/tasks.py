from celery import shared_task
from django.conf import settings

import requests


from account.models import Account


@shared_task(
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
    autoretry_for=(requests.exceptions.RequestException,),
)
def validate_geolocation_holiday(
    account_id, registration_ip_address, date_joined
):
    """Validate geo location holiday."""
    geo_location_url = "https://ipgeolocation.abstractapi.com/v1/?api_key={}&ip_address={}".format(
        settings.ABSTRACT_API_KEY, registration_ip_address
    )

    location = requests.get(geo_location_url)
    location.raise_for_status()
    location = location.json()

    holiday_url = "https://holidays.abstractapi.com/v1/?api_key={}&country={}&year={}&month={}&day={}".format(
        settings.ABSTRACT_API_KEY,
        location.get("country_code", ""),
        date_joined.year,
        date_joined.month,
        date_joined.day,
    )
    response = requests.get(holiday_url)
    response.raise_for_status()
    response = response.json()

    Account.objects.filter(id=account_id).update(
        country=location.get("country"), is_holiday=bool(len(response) > 0)
    )
