from django.urls import path
from django.views.decorators.cache import cache_page

from services.views import (
    ListServicesPageView,
    RandomFilm,
    BlogView,
    ShowPost,
    NewPostView,
    PostUpdateView,
    PostDeleteView,
    UserOrTagBlogView,
    FavoritePosts,
    AddRemoveFavorite,
)

urlpatterns = [
    path(
        "services/", cache_page(60 * 5)(ListServicesPageView.as_view()), name="services"
    ),
    path("services/blog/", BlogView.as_view(), name="blog"),
    path("services/blog/favorites/", FavoritePosts.as_view(), name="favorites"),
    path("post/<slug:post_slug>/", ShowPost.as_view(), name="post"),
    path("services/blog/new_post/", NewPostView.as_view(), name="new_post"),
    path(
        "services/blog/<str:slug>/edit_post/",
        PostUpdateView.as_view(),
        name="edit_post",
    ),
    path(
        "services/blog/<str:nickname>/<int:pk>/",
        UserOrTagBlogView.as_view(),
        name="selected_blog",
    ),
    path(
        "services/blog/<str:name>/",
        UserOrTagBlogView.as_view(),
        name="selected_tag",
    ),
    path("services/blog/<int:pk>/delete/", PostDeleteView.as_view(), name="delete"),
    path(
        "services/blog/<str:nickname>/<int:pk>/add_favorite/",
        AddRemoveFavorite.as_view(),
        name="add_favorite",
    ),
    path("services/film/", cache_page(60 * 5)(RandomFilm.as_view()), name="film"),
]
