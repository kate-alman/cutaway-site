import smtplib
import ssl
from email.message import EmailMessage

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.views import View

from django.views.generic import ListView

from main_body.forms import FeedbackForm
from mino_project.settings import EMAIL_HOST_USER, DEFAULT_FROM_EMAIL, EMAIL_HOST_PASSWORD, RECIPIENTS_EMAIL, \
    EMAIL_HOST, EMAIL_PORT
from services.models import News
from main_body.utils import WeatherMixin


class MainPageView(WeatherMixin, View):
    template_name = "main_body/main_page.html"
    extra_context = {"title": "Main Page"}

    def get(self, request, **kwargs):
        weather = self.get_user_context(request, **kwargs)
        return render(request, "main_body/main_page.html", {"weather": weather})

    def post(self):
        return redirect("home")


class AboutPageView(ListView):
    template_name = "main_body/about.html"
    queryset = News.objects.all().select_related("user")


class FeedbackView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "main_body/feedback.html", {"form": FeedbackForm})

    def post(self, *args, **kwargs):
        msg = EmailMessage()
        msg.set_content(f"{self.request.POST.get('email')}\n{self.request.POST.get('content')}")
        msg["Subject"] = self.request.POST.get("title")
        msg["From"] = DEFAULT_FROM_EMAIL
        msg["To"] = DEFAULT_FROM_EMAIL
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
            smtp.starttls(context=context)
            smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            smtp.send_message(msg, DEFAULT_FROM_EMAIL, DEFAULT_FROM_EMAIL)
            return redirect("home")


class PayView(View):
    def get(self, request):
        return render(request, "main_body/pay.html")


class PayFailView(View):
    def get(self, request):
        return render(request, "main_body/fail.html")


class PaySuccessView(View):
    def get(self, request):
        return render(request, "main_body/success.html")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
