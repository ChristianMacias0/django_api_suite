# Archivo: demo_rest_api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid

# --- BASE DE DATOS EN MEMORIA ---
data_list = []
data_list.append({"id": str(uuid.uuid4()), "name": "User01", "email": "user01@example.com", "is_active": True})
data_list.append({"id": str(uuid.uuid4()), "name": "User02", "email": "user02@example.com", "is_active": True})
data_list.append({"id": str(uuid.uuid4()), "name": "User03", "email": "user03@example.com", "is_active": False})

# --- FUNCIÓN DE AYUDA ---
# Para no repetir la búsqueda del item en cada método
def find_item_by_id(item_id):
    for item in data_list:
        if item['id'] == item_id:
            return item
    return None

# --- VISTA PARA LA COLECCIÓN (/api/) ---
class DemoRestAPI(APIView):
    """
    Maneja la colección de recursos: obtener la lista y crear nuevos.
    """
    def get(self, request, format=None):
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Los campos name y email son requeridos.'}, status=status.HTTP_400_BAD_REQUEST)
        
        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)
        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)

# --- VISTA PARA UN ITEM ESPECÍFICO (/api/<id>/) ---
# ¡NUEVA CLASE AÑADIDA!
class DemoRestApiItem(APIView):
    """
    Maneja un recurso individual: actualizar (PUT, PATCH) y eliminar (DELETE).
    """

    def get(self, request, item_id, format=None):
        item = find_item_by_id(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(item, status=status.HTTP_200_OK)

    def put(self, request, item_id, format=None):
        """Reemplaza completamente el elemento."""
        item = find_item_by_id(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Los campos name y email son requeridos para el reemplazo.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Reemplazar los datos manteniendo el ID y el estado de actividad
        item['name'] = data['name']
        item['email'] = data['email']
        # Opcional: permitir cambiar el estado de actividad si se envía
        item['is_active'] = data.get('is_active', item['is_active'])

        return Response({'message': 'Elemento actualizado exitosamente.', 'data': item}, status=status.HTTP_200_OK)

    def patch(self, request, item_id, format=None):
        """Actualiza parcialmente el elemento."""
        item = find_item_by_id(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        
        # Actualizar solo los campos que se envían
        item['name'] = data.get('name', item['name'])
        item['email'] = data.get('email', item['email'])
        item['is_active'] = data.get('is_active', item['is_active'])

        return Response({'message': 'Elemento actualizado parcialmente.', 'data': item}, status=status.HTTP_200_OK)

    def delete(self, request, item_id, format=None):
        """Elimina lógicamente el elemento (lo desactiva)."""
        item = find_item_by_id(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        item['is_active'] = False
        
        # Se devuelve una respuesta vacía, como es común en DELETE
        return Response(status=status.HTTP_204_NO_CONTENT)