import json
from http import HTTPStatus

import pytest


@pytest.fixture(scope="module")
def request_url():
    return "/api/feed/"


@pytest.fixture
def request_body():
    return {"content": "Test Content"}


@pytest.mark.django_db
def test_success(api_client, request_url, create_user, request_body):
    api_client.force_authenticate(user=create_user)

    response = api_client.post(request_url, data=request_body)

    assert response.status_code == HTTPStatus.CREATED
    assert response.data["content"] == request_body["content"]


@pytest.mark.django_db
def test_without_content(api_client, request_url, create_user, request_body):
    del request_body["content"]
    api_client.force_authenticate(user=create_user)

    response = api_client.post(request_url, data=request_body)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_unauthorized(api_client, request_url, create_user, request_body):
    response = api_client.post(request_url, data=request_body)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
