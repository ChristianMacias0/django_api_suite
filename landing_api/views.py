# Archivo: landing_api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
# ¡Añadimos el import para datetime que ahora sí necesitamos!
from datetime import datetime

class LandingAPI(APIView):
    """
    Vista para realizar operaciones CRUD en la colección de leads de la landing page
    en Firebase Realtime Database.
    """
    
    name = "Landing API"
    collection_name = "landing_leads" # Nombre del nodo en Firebase
    
    def get(self, request, format=None):
        """
        Obtiene todos los elementos de la colección desde Firebase Realtime Database.
        """
        try:
            ref = db.reference(f'/{self.collection_name}')
            data = ref.get()

            if not data:
                return Response([], status=status.HTTP_200_OK)

            if isinstance(data, dict):
                data = list(data.values())
                
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Ocurrió un error al obtener los datos de Firebase: {e}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # === MÉTODO POST AÑADIDO ===
    def post(self, request, format=None):
        """
        Crea un nuevo lead en Firebase Realtime Database.
        """
        # Obtenemos los datos del cuerpo de la solicitud
        data = request.data

        # Validación mínima para asegurar que se envíen datos
        if not data:
            return Response(
                {'error': 'No se recibieron datos en la solicitud.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Obtenemos la referencia a la colección en Firebase
            ref = db.reference(f'/{self.collection_name}')

            # Generamos y formateamos la fecha y hora actual
            current_time  = datetime.now()
            custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
            
            # Añadimos el timestamp a los datos recibidos
            data['timestamp'] = custom_format

            # Usamos push para guardar el objeto en la colección (Firebase genera un ID único)
            new_resource = ref.push(data)

            # Devolvemos el ID único generado por Firebase (la "key")
            return Response({'id': new_resource.key}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': f'Ocurrió un error al guardar los datos en Firebase: {e}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )