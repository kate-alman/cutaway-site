from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from django import forms
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.utils.safestring import mark_safe


class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        try:
            img_html = mark_safe(
                f'<br><br>Current photo: <img src="{value.url}"/ height="100px">'
            )
            return f"{input_html}{img_html}"
        except AttributeError:
            context = self.get_context(name, value, attrs)
            return self._render(self.template_name, context, kwargs.get("renderer"))


def check_max_file_size(value: TemporaryUploadedFile) -> None:
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("File too large. Size should not exceed 5 Mb.")


class FeedbackForm(forms.Form):
    title = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={"class": "form-input"})
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-input", "cols": 60, "rows": 5})
    )
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-select"}))
    captcha = CaptchaField(label="Are you an human?")
