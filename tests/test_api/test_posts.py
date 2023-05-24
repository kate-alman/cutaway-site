import pytest
from django.db import IntegrityError
from django.urls import reverse

from services.models import News


@pytest.mark.django_db
@pytest.mark.parametrize(
    "title, content, image, count",
    (("post", "content", "image", 1), ("post2", "text", "", 1), ("post3", "", "", 1)),
)
def test_create_post(create_user, title, content, image, auto_tag, count):
    user = create_user()
    post = News.objects.create(
        user=user, title=title, content=content, image=image, tag=auto_tag
    )
    assert News.objects.count() == count
    assert user == post.user


def test_create_post_empty_tag(create_user):
    with pytest.raises(IntegrityError):
        News.objects.create(user=create_user(), title="new", tag=None)


@pytest.mark.django_db
def test_create_post_unique_slug(create_user, auto_tag):
    user = create_user()
    post1 = News.objects.create(user=user, title="new", tag=auto_tag)
    assert News.objects.count() == 1
    post2 = News.objects.create(user=user, title="new", tag=auto_tag)
    assert News.objects.count() == 2
    assert post1.slug != post2.slug


@pytest.mark.django_db
def test_create_post_unauthorized(client, post):
    url = reverse("posts")
    response = client.post(url, data=post)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_post_authorized(api_client, post, auto_tag):
    url = reverse("posts")
    response = api_client.post(url, data=post)
    assert response.status_code == 201
    assert News.objects.count() == 1


@pytest.mark.django_db
def test_create_post_author(auto_login_user, post):
    client, user = auto_login_user()
    url = reverse("posts")
    response = client.post(url, data=post)
    assert user.username == response.json().get("user")


@pytest.mark.django_db
def test_edit_post_author(auto_login_user, post):
    client, user = auto_login_user()
    url = reverse("posts")
    response_post = client.post(url, data=post)
    edit_url = reverse("post_info", kwargs={"pk": response_post.json().get("id")})
    data = {
        "title": "new post name",
        "content": response_post.json().get("content"),
        "tag": post.get("tag"),
    }
    response = client.patch(edit_url, json=data)
    assert response.status_code == 200
