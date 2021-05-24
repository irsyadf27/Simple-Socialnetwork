from social_network.settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

REST_FRAMEWORK["TEST_REQUEST_DEFAULT_FORMAT"] = "json"

ABSTRACT_BASE_URL = "url/v1/"
ABSTRACT_GEO_LOCATION_URL = f"https://geolocation.{ABSTRACT_BASE_URL}"
ABSTRACT_HOLIDAY_URL = f"https://holidays.{ABSTRACT_BASE_URL}"
