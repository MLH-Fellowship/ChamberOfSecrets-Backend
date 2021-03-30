import os
from django.shortcuts import render

from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .encryption_decryption.combined import encrypt
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import FileUploadSerializer
from .models import FileUpload 

# Create your views here.
class FileUploadViewSet(APIView):
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request):
        return Response("GET API")


    def post(self, request):
        print("wassup")
        serializer = FileUploadSerializer(data=request.data)
        # print("serializer",request.data)
        # for file_entry in request.FILES.getlist('files'):
        #     uploaded_file_name = file_entry.name
        #     uploaded_file_content = file_entry.read()
        #     print("uploaded file name")
        if serializer.is_valid():
            serializer.save()
            file_path = os.getcwd() + serializer.data['file_uploaded'].replace('/', '\\')
            # print(os.getcwd()+'\media\splits')
            # print(request)
            #request.headers['authorization']
            # import jwt
            # encoded = jwt.encode({"some": "payload"}, settings.SECRET_KEY, algorithm="HS256")
            print("inside serializer.usvalies")
            #pyjwt
            # import jwt
            # jwt.decode(token,settings.SECRET)
            #i need the bearer token
            # #decode this toke and get username
            encrypt(file_path, os.getcwd()+'\media\splits',"0pGPL19ZcYqtY8HWLjbAM8IkBGCHZYz-GTgTxR_9lik=","new")
            """
            Encryption and splitting logic goes here

            """
            # delete file from DB and file storage
            FileUpload.objects.get(file_uploaded = serializer.data['file_uploaded'][7:]).delete()
            if os.path.exists(file_path):
                os.remove(file_path)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

     