from uuid import uuid4

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture(scope="session", autouse=True)
def setup():
    # setup

    # do tests
    yield

    # tear down
