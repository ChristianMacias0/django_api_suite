# Archivo: landing_api/urls.py
from django.urls import path
from .views import LandingAPI

# Este nombre es crucial para la plantilla de DRF.
urlpatterns = [
    path("", LandingAPI.as_view(), name="api-root"),
]