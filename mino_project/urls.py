"""mino_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from main_body.views import page_not_found
from mino_project import settings
from project_api.swagger_generator import CustomOpenAPISchemaGenerator

schema_view = get_schema_view(
    openapi.Info(
        title="Alman Project API",
        default_version="v1",
        description="Convenient access to the data of the site 'kate alman project'.<br> "
        "View all data, manage your posts and data.",
        contact=openapi.Contact(email="ekaterina.aman@syandex.ru"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated],
    generator_class=CustomOpenAPISchemaGenerator,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main_body.urls")),
    path("accounts/", include("accounts.urls")),
    path("api/", include("project_api.urls")),
    path("", include("services.urls")),
    path("captcha/", include("captcha.urls")),
    re_path(
        r"swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

if settings.DEBUG:
    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
