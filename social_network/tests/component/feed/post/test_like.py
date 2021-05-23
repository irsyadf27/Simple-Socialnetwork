import json
from http import HTTPStatus
import pytest
from django.utils import timezone

from account.models import Account
from feed.models import FeedPost


@pytest.fixture(scope="module")
def request_url():
    return "/api/feed/feed/1/like/"


@pytest.fixture(autouse=True)
def setup_feed():
    user1 = Account.objects.create(
        id=1,
        username="test1",
        email="test1@test.com",
        first_name="test",
        last_name="test",
    )

    user1.set_password("testtest2")
    user1.save()

    user2 = Account.objects.create(
        id=2,
        username="test2",
        email="test2@test.com",
        first_name="test",
        last_name="test",
    )

    user2.set_password("testtest2")
    user2.save()

    FeedPost.objects.create(
        id=1,
        creator=user1,
        content="Test User 1",
        created_at=timezone.now()
    )

    FeedPost.objects.create(
        id=2,
        creator=user2,
        content="Test User 1",
        created_at=timezone.now()
    )


@pytest.fixture
def auth_user1():
    return Account.objects.get(id=1)
  

@pytest.fixture
def auth_user2():
    return Account.objects.get(id=2)


@pytest.mark.django_db
def test_success(api_client, request_url, auth_user1):
    api_client.force_authenticate(user=auth_user1)

    response = api_client.post(request_url)
    response_dict = json.loads(response.content)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_duplicate_like(api_client, request_url, auth_user1):
    api_client.force_authenticate(user=auth_user1)

    response = api_client.post(request_url)
    response_dict = json.loads(response.content)

    assert response.status_code == HTTPStatus.OK

    response2 = api_client.post(request_url)
    response_dict2 = json.loads(response.content)

    assert response2.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_unauthorized(api_client, request_url, auth_user1):
    response = api_client.post(request_url)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
