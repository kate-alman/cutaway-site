from django.http import HttpRequest
from django.middleware.common import MiddlewareMixin
from django.db.models import F
from django.db import transaction

from main_body.models import PageVisits


class CounterMiddleware(MiddlewareMixin):
    IGNORED_URL = ("/captcha", "/media", "/login", "/register", "/accounts")

    def process_request(self, request: HttpRequest) -> None:
        if not request.path.startswith(self.IGNORED_URL):
            if not request.session.session_key:
                request.session.save()

            session_key = request.session.session_key
            with transaction.atomic():
                counter, created = PageVisits.objects.get_or_create(url=request.path)
                if session_key and counter.session_id != session_key:
                    counter.session_id = session_key
                    counter.count = F("count") + 1
                    counter.save()
