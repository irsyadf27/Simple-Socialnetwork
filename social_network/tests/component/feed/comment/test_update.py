import json
from http import HTTPStatus
import pytest
from django.utils import timezone

from account.models import Account
from feed.models import FeedPost, FeedComment


@pytest.fixture(scope="module")
def request_url():
    return "/api/feed/comment/1/"


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

    post1 = FeedPost.objects.create(
        id=1,
        creator=user1,
        content="Test User 1",
        created_at=timezone.now()
    )

    post2 = FeedPost.objects.create(
        id=2,
        creator=user2,
        content="Test User 1",
        created_at=timezone.now()
    )

    comment1 = FeedComment.objects.create(
        id=1,
        post=post1,
        creator=user1,
        comment="Test Comment 1",
        created_at=timezone.now()
    )

    comment2 = FeedComment.objects.create(
        id=2,
        post=post1,
        creator=user2,
        comment="Test Comment 2",
        created_at=timezone.now()
    )


@pytest.fixture
def request_body():
    return {
        "post": 1,
        "comment": "Test Update Comment"
    }


@pytest.fixture
def auth_user1():
    return Account.objects.get(id=1)
  

@pytest.fixture
def auth_user2():
    return Account.objects.get(id=2)


@pytest.mark.django_db
def test_success(api_client, request_url, auth_user1, request_body):
    api_client.force_authenticate(user=auth_user1)

    response = api_client.put(request_url, data=request_body)
    response_dict = json.loads(response.content)

    assert response.status_code == HTTPStatus.OK
    assert response_dict["comment"] == request_body["comment"]


@pytest.mark.django_db
def test_without_comment(api_client, request_url, auth_user1, request_body):
    del request_body["comment"]
    api_client.force_authenticate(user=auth_user1)

    response = api_client.put(request_url, data=request_body)
    response_dict = json.loads(response.content)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_update_another_user(api_client, request_url, auth_user2, request_body):
    api_client.force_authenticate(user=auth_user2)

    response = api_client.put(request_url, data=request_body)
    response_dict = json.loads(response.content)

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_partial_success(api_client, request_url, auth_user1, request_body):
    api_client.force_authenticate(user=auth_user1)

    response = api_client.patch(request_url, data=request_body)
    response_dict = json.loads(response.content)

    assert response.status_code == HTTPStatus.OK
    assert response_dict["comment"] == request_body["comment"]


@pytest.mark.django_db
def test_partial_without_content(api_client, request_url, auth_user1, request_body):
    del request_body["comment"]
    api_client.force_authenticate(user=auth_user1)

    response = api_client.patch(request_url, data=request_body)
    response_dict = json.loads(response.content)

    assert response.status_code == HTTPStatus.OK
    assert response_dict["comment"] == "Test Comment 1"


@pytest.mark.django_db
def test_partial_update_another_user(api_client, request_url, auth_user2, request_body):
    api_client.force_authenticate(user=auth_user2)

    response = api_client.patch(request_url, data=request_body)
    response_dict = json.loads(response.content)

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_unauthorized(api_client, request_url, auth_user1, request_body):
    response = api_client.put(request_url, data=request_body)
    response_dict = json.loads(response.content)

    assert response.status_code == HTTPStatus.UNAUTHORIZED