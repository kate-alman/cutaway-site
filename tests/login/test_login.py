import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user("user", "user@mail.com", "password")
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_unique_user_create():
    User.objects.create_user("user", "user@mail.com", "password")
    with pytest.raises(IntegrityError):
        User.objects.create_user("user", "user2@mail.com", "password")


@pytest.mark.django_db
def test_unique_email_create():
    User.objects.create_user("user", "user@mail.com", "password")
    with pytest.raises(IntegrityError):
        User.objects.create_user("user2", "user@mail.com", "password")


@pytest.mark.django_db
def test_docs_unauthorized(client):
    url = reverse("schema-swagger-ui")
    response = client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_docs_authorized(auto_login_user):
    client, user = auto_login_user()
    url = reverse("schema-swagger-ui")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_as_admin(admin_client):
    url = reverse("schema-swagger-ui")
    response = admin_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_detail(auto_login_user):
    client, user = auto_login_user()
    url = reverse("user_detail", kwargs={"username": user.username})
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert user.username in response.request["PATH_INFO"]


@pytest.mark.django_db
def test_user_detail_unavailable(auto_login_user):
    client, user = auto_login_user()
    url = reverse("user_detail", kwargs={"username": "someone"})
    response = client.get(url, follow=True)
    assert response.status_code == 404
