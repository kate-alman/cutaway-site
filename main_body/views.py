from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.views import View

from django.views.generic import ListView

from main_body.forms import FeedbackForm
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

    def post(self):
        return redirect("home")

    def form_valid(self, form):
        if form.is_valid():
            form.save()
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
