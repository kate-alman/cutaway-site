import uuid

import pytest

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from services.models import Tag, News


@pytest.fixture
def test_password():
    return "Strong-test-pass123"


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "username" not in kwargs:
            kwargs["username"] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user

    return make_auto_login


@pytest.fixture
def api_client(create_user):
    user = create_user()
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def auto_tag():
    tag = Tag.objects.create(name="tag")
    return tag


@pytest.fixture
def post(auto_tag):
    data = {"user": "username", "title": "post name", "content": "", "tag": auto_tag.pk}
    return data


@pytest.fixture
def user_post(auto_tag, create_user):
    post = News.objects.create(
        user=create_user(username="new_user"),
        title="post",
        content="content",
        tag=auto_tag,
    )
    return post
