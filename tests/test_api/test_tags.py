import pytest
from django.db import IntegrityError
from django.urls import reverse

from services.models import Tag


@pytest.mark.django_db
@pytest.mark.parametrize(
    "tag_names, count",
    ((["tag"], 1), (["tag", "tag2"], 2), (["tag", "tag2", "tag3", "tag4", "tag5"], 5)),
)
def test_tag_create(tag_names, count):
    for tag_name in tag_names:
        Tag.objects.create(name=tag_name)
    assert Tag.objects.count() == count


@pytest.mark.django_db
def test_create_tag_unique():
    Tag.objects.create(name="new-tag")
    assert Tag.objects.count() == 1

    with pytest.raises(IntegrityError):
        Tag.objects.create(name="new-tag")


@pytest.mark.django_db
def test_create_tag_unauthorized(client):
    url = reverse("tags")
    data = {"name": "tag-test"}
    response = client.post(url, data=data)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_tag_authorized(api_client):
    url = reverse("tags")
    data = {"name": "tag-test"}
    response = api_client.post(url, data=data)
    assert response.status_code == 201
    assert Tag.objects.count() == 1


@pytest.mark.django_db
def test_create_empty_tag(api_client):
    url = reverse("tags")
    data = {"name": ""}
    response = api_client.post(url, data=data)
    assert response.status_code == 400
    assert Tag.objects.count() == 0
