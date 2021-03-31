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
from django.conf import settings
import jwt

# Create your views here.
class FileUploadViewSet(APIView):
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request):
        return Response("GET API")


    def post(self, request):
        print("wassup")
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            file_path = os.getcwd() + serializer.data['file_uploaded'].replace('/', '\\')
            jwt_token=request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            jwt_token=jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
            print("headers",request.data['private_key'])
            encrypt(file_path, os.getcwd()+'\media\splits',request.data['private_key'],jwt_token['username'])
            """
            Encryption and splitting logic goes here

            """
            # delete file from DB and file storage
            FileUpload.objects.get(file_uploaded = serializer.data['file_uploaded'][7:]).delete()
            if os.path.exists(file_path):
                os.remove(file_path)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

     