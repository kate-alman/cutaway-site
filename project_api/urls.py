from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from project_api.views import (
    NewsAPIList,
    PostAPIUpdate,
    UsersAPIList,
    ProfileAPIUpdate,
    UserPostsAPIList,
    TagAPIList,
)


urlpatterns = [
    path("v1/posts/", NewsAPIList.as_view(), name="posts"),
    path("v1/tags/", TagAPIList.as_view(), name="tags"),
    path("v1/post/<int:pk>/", PostAPIUpdate.as_view(), name="post_info"),
    path("v1/user-posts/<int:pk>/", UserPostsAPIList.as_view(), name="user-posts"),
    path("v1/users/", UsersAPIList.as_view(), name="users"),
    path("v1/user/<int:pk>/", ProfileAPIUpdate.as_view(), name="user_info"),
    path("v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
