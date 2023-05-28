from django.urls import path

from django.contrib.auth.views import (
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView,
)

from accounts.views import (
    RegisterUser,
    LoginUser,
    logout_user,
    UserProfileView,
    UserPasswordChangeView,
    UserDeleteView,
    UpdateUserProfile,
)

urlpatterns = [
    path("login/", LoginUser.as_view(), name="login"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("logout/", logout_user, name="logout"),
    path(
        "login/password_reset/",
        PasswordResetView.as_view(template_name="accounts/password_reset_form.html"),
        name="password_reset",
    ),
    path(
        "login/password_reset/done/",
        PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "login/password_reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        "login/password_reset_complete/",
        PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path("<str:username>/", UserProfileView.as_view(), name="user_detail"),
    path(
        "profile/<str:slug>/change_info/",
        UpdateUserProfile.as_view(),
        name="change_info",
    ),
    path(
        "profile/password-change/",
        UserPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "profile/password-change-done/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("profile/<int:pk>/user_delete/", UserDeleteView.as_view(), name="user_delete"),
]
