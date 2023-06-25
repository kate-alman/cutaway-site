from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from accounts.models import Profile
from main_body.forms import ImagePreviewWidget, check_max_file_size


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label="Login",
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "Enter login"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-input", "placeholder": "Enter email"}
        ),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-input", "placeholder": "Enter password"}
        ),
    )
    password2 = forms.CharField(
        label="Password again",
        widget=forms.PasswordInput(
            attrs={"class": "form-input", "placeholder": "Enter password again"}
        ),
    )
    captcha = CaptchaField(label="Are you human?")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="Login",
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "Enter login"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-input", "placeholder": "Enter password"}
        ),
    )
    captcha = CaptchaField(label="Are you human?")


class UpdateProfileForm(forms.ModelForm):
    """Updating the user profile in the personal account."""
    photo = forms.ImageField(
        widget=ImagePreviewWidget, validators=[check_max_file_size]
    )

    class Meta:
        model = Profile
        fields = ("nickname", "bio", "location", "birth_date", "photo")
        widgets = {
            "nickname": forms.TextInput(attrs={"class": "form-input"}),
            "bio": forms.Textarea(attrs={"class": "form-input", "cols": 60, "rows": 7}),
            "location": forms.TextInput(attrs={"class": "form-input"}),
            "birth_date": forms.SelectDateWidget(years=(range(1950, 2023))),
        }


class UserPasswordChangeForm(SetPasswordForm):
    """Updating the user password in the personal account."""
    captcha = CaptchaField(label="Are you human?")
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "off",
                "placeholder": "Enter new password",
            }
        ),
    )
    new_password2 = forms.CharField(
        label="New password again",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "off",
                "placeholder": "Enter new password again",
            }
        ),
    )
