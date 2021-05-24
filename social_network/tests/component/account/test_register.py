from http import HTTPStatus

import pytest
from celery_mock import task_mock


@pytest.fixture(scope="module")
def request_url():
    return "/api/account/register/"


@pytest.fixture
def request_body():
    return {
        "username": "Test",
        "password": "testtest2",
        "confirm_password": "testtest2",
        "email": "test@test.com",
        "first_name": "test",
        "last_name": "test",
    }


@pytest.mark.django_db
def test_success(api_client, request_url, request_body):
    response = api_client.post(request_url, data=request_body)

    assert response.status_code == HTTPStatus.CREATED
    assert response.data["username"] == request_body["username"]


@pytest.mark.django_db
def test_without_username(api_client, request_url, request_body):
    del request_body["username"]
    response = api_client.post(request_url, data=request_body)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_blank_username(api_client, request_url, request_body):
    request_body["username"] = ""
    response = api_client.post(request_url, data=request_body)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_without_password(api_client, request_url, request_body):
    del request_body["password"]
    response = api_client.post(request_url, data=request_body)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_blank_password(api_client, request_url, request_body):
    request_body["password"] = ""
    response = api_client.post(request_url, data=request_body)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_min_length_password(api_client, request_url, request_body):
    request_body["password"] = "123"
    response = api_client.post(request_url, data=request_body)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_without_confirm_password(api_client, request_url, request_body):
    del request_body["confirm_password"]
    response = api_client.post(request_url, data=request_body)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_blank_confirm_password(api_client, request_url, request_body):
    request_body["confirm_password"] = ""
    response = api_client.post(request_url, data=request_body)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_min_length_confirm_password(api_client, request_url, request_body):
    request_body["confirm_password"] = "123"
    response = api_client.post(request_url, data=request_body)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_confirm_password_not_same(api_client, request_url, request_body):
    request_body["confirm_password"] = "123"
    response = api_client.post(request_url, data=request_body)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_without_email(api_client, request_url, request_body):
    del request_body["email"]
    response = api_client.post(request_url, data=request_body)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_blank_email(api_client, request_url, request_body):
    request_body["email"] = ""
    response = api_client.post(request_url, data=request_body)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_invalid_email(api_client, request_url, request_body):
    request_body["email"] = "INVALID"
    response = api_client.post(request_url, data=request_body)

    assert response.status_code == HTTPStatus.BAD_REQUEST