from django.urls import path
from django.views.decorators.cache import cache_page

from main_body.views import (
    MainPageView,
    AboutPageView,
    FeedbackView,
    PayView,
    PaySuccessView,
    PayFailView,
)

urlpatterns = [
    path("", MainPageView.as_view(), name="home"),
    path("about/", cache_page(60 * 5)(AboutPageView.as_view()), name="about"),
    path("pay/", PayView.as_view(), name="pay"),
    path("pay/success/", PaySuccessView.as_view(), name="success"),
    path("pay/fail/", PayFailView.as_view(), name="fail"),
    path("feedback/", FeedbackView.as_view(), name="feedback"),
]
