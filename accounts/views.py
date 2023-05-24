from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, Http404, HttpRequest
from django.shortcuts import redirect, get_object_or_404, render

from django.urls import reverse_lazy
from django.contrib.auth import logout, login
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetDoneView,
)
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from accounts.forms import (
    RegisterUserForm,
    LoginUserForm,
    UpdateProfileForm,
    UserPasswordChangeForm,
)
from accounts.models import Profile
from main_body.utils import WeatherMixin
from services.utils import UserMixin


class RegisterUser(WeatherMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        user.profile.nickname = user.username
        user.profile.save()
        login(self.request, user)
        return redirect("home")


class LoginUser(WeatherMixin, LoginView):
    form_class = LoginUserForm
    template_name = "accounts/login.html"

    def get_success_url(self):
        return reverse_lazy("home")


class ResetPasswordDoneView(PasswordResetDoneView):
    success_url = reverse_lazy("login")


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = "accounts/password_change_form.html"

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        resp_body = '<script>alert("Password changed");\
                                window.location="%s"</script>'
        return HttpResponse(resp_body % reverse_lazy("login"))


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("home")


def logout_user(request):
    logout(request)
    return redirect("login")


class UserProfileView(LoginRequiredMixin, UserMixin, View):
    model = Profile
    template_name = "accounts/user_profile.html"
    success_url = reverse_lazy("home")
    context_object_name = "user_info"

    def get(self, request: HttpRequest, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        if self.request.user.username == user.username:
            kwargs = kwargs | {"pk": user.pk, "self_profile": True}
            user_info = self.get_user_context(**kwargs)
            return render(request, "accounts/user_profile.html", user_info)
        else:
            raise Http404()


class UpdateUserProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "accounts/change_user_info.html"
    slug_field = "nickname"

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user_id=self.request.user.pk)

    def form_valid(self, form):
        form.save()
        resp_body = '<script>alert("Profile changed");\
                                                     window.location="%s"</script>'
        slug = self.kwargs.get("slug", None)
        return HttpResponse(
            resp_body
            % (
                reverse_lazy("user_detail", kwargs={"username": slug})
                if slug
                else reverse_lazy("home")
            )
        )
