# Archivo: landing_api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime

class LandingAPI(APIView):
    """
    Vista para interactuar con los datos de productos en Firebase Realtime Database.
    """

    name = "Landing API"
    collection_name = "productosmasvistos" # Correcto, apunta a tu nodo

    def get(self, request, format=None):
        """
        Obtiene los productos y sus contadores desde Firebase,
        formateándolos en una lista de objetos.
        """
        try:
            ref = db.reference(f'/{self.collection_name}')
            data = ref.get()

            if not data:
                return Response([], status=status.HTTP_200_OK)

            # --- LÓGICA CORREGIDA ---
            # Vamos a transformar el diccionario de Firebase en una lista de diccionarios más útil

            processed_data = []
            for key, value in data.items():
                # Solo procesamos las entradas que tienen la estructura de un producto con contador
                # Esto ignora la entrada antigua con el ID '-OWGc...'
                if isinstance(value, dict) and 'count' in value:
                    processed_data.append({
                        'product_name': key,      # La clave es el nombre del producto
                        'view_count': value['count'] # El valor del contador
                    })

            # Opcional: Ordenar la lista de más a menos vistos
            processed_data.sort(key=lambda x: x['view_count'], reverse=True)

            return Response(processed_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Ocurrió un error al obtener los datos de Firebase: {e}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # Tu método POST puede quedar como está, aunque ahora mismo está diseñado
    # para guardar leads y no para actualizar contadores de productos.
    # Si quieres mantenerlo, no hay problema.
    def post(self, request, format=None):
        # ... (tu código post actual) ...
        data = request.data
        if not data:
            return Response({'error': 'No se recibieron datos en la solicitud.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ref = db.reference(f'/{self.collection_name}')
            current_time  = datetime.now()
            custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
            data['timestamp'] = custom_format
            new_resource = ref.push(data)
            return Response({'id': new_resource.key}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Ocurrió un error al guardar los datos en Firebase: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)