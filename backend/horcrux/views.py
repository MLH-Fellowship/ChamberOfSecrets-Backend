import os
from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .encryption_decryption.combined import encrypt
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import FileUploadSerializer, FileDataSerializer
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
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # file encryption and splitting
            file_path = os.getcwd() + serializer.data['file_uploaded'].replace('/', '\\')  # getting file path
            jwt_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]  
            jwt_token = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
            encrypt(file_path, os.getcwd()+'\media\splits', request.data['private_key'], jwt_token['username'])

            # creating a log in FileData db table
            user = User.objects.get(username=jwt_token['username'])
            file_name = serializer.data['file_uploaded'][13:] 
            split_1 = 'dummy text'  # Replace w/ url or fileId for the storage platform
            split_2 = 'dummy text'
            split_3 = 'dummy text'
            file_data = {'file_name':file_name, 'split_1':split_1, 'split_2':split_2,'split_3':split_3}
            serializer_filedata = FileDataSerializer(data=file_data)
            if serializer_filedata.is_valid():
                serializer_filedata.save(username=user)  # creates FileData instance

            # delete file from DB and file storage
            FileUpload.objects.get(file_uploaded = serializer.data['file_uploaded'][7:]).delete()
            if os.path.exists(file_path):
                os.remove(file_path)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

     