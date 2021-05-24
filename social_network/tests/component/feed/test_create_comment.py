import json
from http import HTTPStatus
import pytest
from django.utils import timezone

from account.models import Account
from feed.models import FeedPost, FeedComment


@pytest.fixture(scope="module")
def request_url():
    return "/api/feed/1/comments/add/"


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
        id=1, creator=user1, content="Test User 1", created_at=timezone.now()
    )

    FeedPost.objects.create(
        id=2, creator=user2, content="Test User 1", created_at=timezone.now()
    )


@pytest.fixture
def request_body():
    return {"post": 1, "comment": "Test Comment"}


@pytest.mark.django_db
def test_success(api_client, request_url, create_user, request_body):
    api_client.force_authenticate(user=create_user)

    response = api_client.post(request_url, data=request_body)
    response_dict = json.loads(response.content)

    assert response.status_code == HTTPStatus.OK
    assert response_dict["comment"] == request_body["comment"]


@pytest.mark.django_db
def test_without_comment(api_client, request_url, create_user, request_body):
    del request_body["comment"]
    api_client.force_authenticate(user=create_user)

    response = api_client.post(request_url, data=request_body)
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_unauthorized(api_client, request_url, create_user, request_body):
    response = api_client.post(request_url, data=request_body)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
