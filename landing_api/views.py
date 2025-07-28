from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "productosmasvistos"  # Cambia este nombre según tu colección en Firebase

    def get(self, request):
        ref = db.reference(self.collection_name)
        data = ref.get()
        result = []
        if isinstance(data, dict):
            for producto, atributos in data.items():
                item = {"producto": producto}
                if isinstance(atributos, dict):
                    item.update(atributos)
                result.append(item)
        elif data is None:
            result = []
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request):
        obj = request.data.copy()
        now = datetime.now()
        timestamp = now.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace("am", "a. m.").replace("pm", "p. m.")
        obj["timestamp"] = timestamp
        ref = db.reference(self.collection_name)
        new_ref = ref.push(obj)
        return Response({"id": new_ref.key}, status=status.HTTP_201_CREATED)
