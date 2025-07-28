# Archivo: landing_api/urls.py

from django.urls import path
from .views import LandingAPI

urlpatterns = [
    path("", LandingAPI.as_view(), name="landing_api_collection"),
]