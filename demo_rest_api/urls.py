# demo_rest_api/urls.py
from django.urls import path
from .views import DemoRestAPI, DemoRestApiItem

app_name = 'demo_rest_api'

urlpatterns = [
    path("", DemoRestAPI.as_view(), name="demo_rest_api_collection"),
    path("<str:item_id>/", DemoRestApiItem.as_view(), name="demo_rest_api_item"),
]