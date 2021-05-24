import json
from http import HTTPStatus

import pytest


from account.models import Account


@pytest.fixture(scope="module")
def request_url():
    return "/api/account/auth-token/"


@pytest.fixture(autouse=True)
def setup_account():
    user = Account.objects.create(
        username="test",
        email="test@test.com",
        first_name="test",
        last_name="test",
    )

    user.set_password("testtest2")
    user.save()


@pytest.fixture
def request_body():
    return {"username": "test", "password": "testtest2"}


@pytest.mark.django_db
def test_success(api_client, request_url, request_body):
    response = api_client.post(request_url, data=request_body)
    response_dict = json.loads(response.content)

    assert response.status_code == HTTPStatus.OK
    assert "access" in response_dict


@pytest.mark.django_db
def test_invalid_credential(api_client, request_url, request_body):
    request_body["username"] = "INVALID"
    response = api_client.post(request_url, data=request_body)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.django_db
def test_without_username(api_client, request_url, request_body):
    del request_body["username"]
    response = api_client.post(request_url, data=request_body)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_without_password(api_client, request_url, request_body):
    del request_body["password"]
    response = api_client.post(request_url, data=request_body)

    assert response.status_code == HTTPStatus.BAD_REQUEST