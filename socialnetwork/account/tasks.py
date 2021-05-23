import base64
import os

import requests
from datetime import datetime
from celery import shared_task
from requests import HTTPError
from .models import Account


class GeolocationException(Exception):
    pass


class GeolocationUpdateException(Exception):
    pass


class HolidayException(Exception):
    pass


class HolidayUpdateException(Exception):
    pass


class EmailException(Exception):
    pass


@shared_task(
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def geolocation_holiday(account_id: int, ip: str, date_joined: datetime):
    url = "https://ipgeolocation.abstractapi.com/v1/?api_key=d19303c099a24b09b5694dc493fe1788&ip_address={}".format(ip)
    response = requests.get(url)

    try:
        response.raise_for_status()   
        response_json = response.json()     
    except HTTPError:
        raise GeolocationException()

    try:
        Account.objects.filter(id=account_id).update(country=response_json["country"])
    except:
        raise GeolocationUpdateException()

    url_holiday = "https://holidays.abstractapi.com/v1/?api_key=1bd958de6a404843b32f803f0d7dc0ad&country={}&year={}&month={}&day={}".format(response_json["country_code"], date_joined.year, date_joined.month, date_joined.day)
    response_holiday = requests.get(url_holiday)
    is_holiday = False

    try:
        response_holiday.raise_for_status()   
        response_holiday_json = response_holiday.json()
        is_holiday = len(response_holiday_json) > 0
    except HTTPError:
        raise GeolocationException()

    try:
        Account.objects.filter(id=account_id).update(is_holiday=is_holiday)
    except:
        raise GeolocationUpdateException