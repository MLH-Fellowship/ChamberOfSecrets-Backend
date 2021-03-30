import os
from django.shortcuts import render

from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import FileUploadSerializer
from .models import FileUpload 

# Create your views here.
class FileUploadViewSet(APIView):
    serializer_class = FileUploadSerializer

    def list(self, request):
        return Response("GET API")

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            file_path = os.getcwd() + serializer.data['file_uploaded'].replace('/', '\\')
            """
            Encryption and splitting logic goes here

            """
            # delete file from DB and file storage
            FileUpload.objects.get(file_uploaded = serializer.data['file_uploaded'][7:]).delete()
            if os.path.exists(file_path):
                os.remove(file_name)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

     