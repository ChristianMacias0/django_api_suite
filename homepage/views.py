# Archivo: homepage/views.py

from django.shortcuts import render

def index(request):
    # Creamos un diccionario de contexto para pasar datos a la plantilla.
    context = {
        'page_title': 'Página Principal de la API',
        'page_description': 'Esta es la página principal (homepage) de la API que proporciona datos para el Dashboard de un sitio de venta de productos.',
    }
    # Le decimos a Django que renderice el archivo index.html de la app homepage.
    return render(request, 'homepage/index.html', context)