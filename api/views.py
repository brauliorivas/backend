from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
	
from firebase_admin import db


# Create your views here.

class LandingAPI(APIView):
    name = 'Landing API'
     # Coloque el nombre de su colección en el Realtime Database
    collection_name = 'newsletter'

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

    collection_name = 'newsletter'

    def get(self, request, pk):
        ref = db.reference(f'{self.collection_name}')
        record = ref.child(pk).get()

        if record != None:
            return Response(record, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
   

    def put(self, request, pk):
        ref = db.reference(f'{self.collection_name}')
        record = ref.child(pk)
        
        if record.get() == None:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        try:
            email = request.data.get('email')
            motivation = request.data.get('motivation')

            assert type(email) == str
            assert type(motivation) == str

            current_time  = datetime.now()
            custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')

            record.update({"email": email, "motivation": motivation, "saved": custom_format})

            return Response({"result": "correctly updated"}, status= status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        

    def delete(self, request, pk):
        ref = db.reference(f'{self.collection_name}')
        collection_data = ref.get()
        record = collection_data.get(pk)
 
        if record == None:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        ref.child(pk).delete()

        return Response({"result": "correctly removed"}, status=status.HTTP_204_NO_CONTENT)



