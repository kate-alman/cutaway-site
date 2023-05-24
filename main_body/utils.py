import os

import requests
from django.http import HttpRequest
from geopy.geocoders import Nominatim

from main_body.models import Weather


class WeatherMixin:
    API_KEY = os.environ.get("API_KEY")
    BASE_URL = os.environ.get("BASE_URL")
    API_KEY_IP = os.environ.get("API_KEY_IP")
    BASE_URL_IP = os.environ.get("BASE_URL_IP")
    PRIVATE_IPS_PREFIX = ("10.", "172.", "192.", "127.")

    def get_user_context(self, request: HttpRequest, **kwargs) -> dict:
        context = kwargs
        weather = self.get_current_weather(request)
        context["weather"] = weather
        return context

    def get_current_weather(self, request: HttpRequest) -> Weather | str:
        ip = self.get_client_ip(request)
        if ip.get("city"):
            geolocator = Nominatim(user_agent="mino_project")
            location = geolocator.geocode(ip["city"])
            cur_weather = requests.get(
                f"{self.BASE_URL}lat={location.latitude}&lon={location.longitude}"
                f"&appid={self.API_KEY}&units=metric"
            ).json()
            weather = Weather(
                address=ip["city"],
                temp=int(cur_weather["main"]["temp"]),
                feels_like=int(cur_weather["main"]["feels_like"]),
                humidity=cur_weather["main"]["humidity"],
                wind=int(cur_weather["wind"]["speed"]),
                clouds=cur_weather["weather"][0]["description"],
            )
        else:
            weather = "Weather unavailable"
        return weather

    def get_client_ip(self, request: HttpRequest) -> dict:
        remote_address = request.META.get("REMOTE_ADDR")
        ip = remote_address
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            proxies = x_forwarded_for.split(",")
            while len(proxies) > 0 and proxies[0].startswith(self.PRIVATE_IPS_PREFIX):
                proxies.pop(0)
            if len(proxies) > 0:
                ip = proxies[0]
        ip = requests.get(f"{self.BASE_URL_IP}{ip}?access_key={self.API_KEY_IP}").json()
        return ip
