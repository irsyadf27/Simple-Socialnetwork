import pytest
from rest_framework.test import APIClient


from account.models import Account


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    user = Account.objects.create(
        username="test",
        email="test@test.com",
        first_name="User",
        last_name="1",
    )

    user.set_password("testtest123")
    user.save()

    return user


@pytest.fixture(scope="session", autouse=True)
def setup():
    # setup

    # do tests
    yield

    # tear down
