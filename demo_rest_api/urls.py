# Archivo: demo_rest_api/urls.py

from django.urls import path
from .views import DemoRestAPI, DemoRestApiItem # ¡Importa la nueva clase!

urlpatterns = [
    # Ruta para la colección de recursos
    path("", DemoRestAPI.as_view(), name="demo_rest_api_collection"),
    
    # ¡NUEVA RUTA AÑADIDA!
    # Ruta para un recurso individual, identificado por su ID
    path("<str:item_id>/", DemoRestApiItem.as_view(), name="demo_rest_api_item"),
]