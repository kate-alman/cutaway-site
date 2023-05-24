from captcha.fields import CaptchaField
from django import forms

from main_body.forms import ImagePreviewWidget, check_max_file_size
from services.models import News


class NewPostForm(forms.ModelForm):
    captcha = CaptchaField(label="Are you an human?")
    image = forms.ImageField(
        help_text="Image (max size: 5Mb)",
        validators=[check_max_file_size],
        required=False,
    )

    class Meta:
        model = News
        fields = (
            "title",
            "content",
            "image",
            "tag",
        )
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(
                attrs={"class": "form-input", "cols": 60, "rows": 7}
            ),
            "tag": forms.Select(attrs={"class": "form-select"}),
        }


class UpdatePostForm(forms.ModelForm):
    image = forms.ImageField(
        help_text="Image (max size: 5Mb)",
        widget=ImagePreviewWidget,
        validators=[check_max_file_size],
    )

    class Meta:
        model = News
        fields = ("title", "content", "tag", "image")

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(
                attrs={"class": "form-input", "cols": 60, "rows": 7}
            ),
            "tag": forms.Select(attrs={"class": "form-select"}),
        }
