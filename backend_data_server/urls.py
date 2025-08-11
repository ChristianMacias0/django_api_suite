# Archivo: backend_data_server/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Incluye las URLs de la homepage.
    path('homepage/', include('homepage.urls')),

    # Incluye las URLs de autenticación de DRF.
    # Esto es NECESARIO para que la plantilla de DRF funcione.
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Finalmente, incluye las URLs de tu API principal.
    # Esta debe ser la última para que no interfiera con otras rutas.
    path('', include('landing_api.urls')),
]