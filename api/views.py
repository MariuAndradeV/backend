from django.shortcuts import render

# Create your views here.
# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime

from firebase_admin import db

class LandingAPI(APIView):
    
    name = 'Landing API'

    # Coloque el nombre de su colección en el Realtime Database
    collection_name = 'usuarios'

    def get(self, request):

        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}')
        
        # get: Obtiene todos los elementos de la colección
        data = ref.get()

        # Devuelve un arreglo JSON
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
	        
        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}')

        current_time  = datetime.now()
        custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
        request.data.update({"saved": custom_format })
        
        # push: Guarda el objeto en la colección
        new_resource = ref.push(request.data)
        
        # Devuelve el id del objeto guardado
        return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)

class LandingAPIDetail(APIView):
    name = 'Landing Detail API'

    collection_name = 'usuarios'

    def get(self, request, pk):
        ref = db.reference(f'{self.collection_name}')
        documento = ref.get().get(pk)

        if documento:
            return Response(documento, status=status.HTTP_200_OK)
        else:
            return Response('No se encuentra el documento', status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        ref = db.reference(f'{self.collection_name}')

        documento = ref.get().get(pk)

        if not documento:
            return Response('No se encuentra el documento', status=status.HTTP_404_NOT_FOUND)

        if 'email' not in request.data:
            return Response('La petición no tiene los campos requeridos', status=status.HTTP_400_BAD_REQUEST)

        for k, v in request.data.items():
            if k in documento:
                documento[k] = v

        ref.child(pk).set(documento)

        return Response('Item actualizado', status=status.HTTP_200_OK)

    def delete(self, request, pk):
        ref = db.reference(f'{self.collection_name}')

        documento = ref.get().get(pk)
        if not documento:
            return Response('No se encuentra el documento', status=status.HTTP_404_NOT_FOUND)

        ref.child(pk).delete()
        return Response('Se ha eliminado el documento', status=status.HTTP_200_OK)


