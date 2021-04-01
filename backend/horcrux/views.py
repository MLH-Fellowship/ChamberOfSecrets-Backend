import os
from django.shortcuts import render

from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from .encryption_decryption.combined import encrypt,decrypt
from rest_framework.decorators import api_view
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
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            file_path = os.getcwd() + serializer.data['file_uploaded'].replace('/', '\\')
            jwt_token=request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            jwt_token=jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
            encrypt(file_path, os.getcwd()+'\media\splits',request.data['private_key'],jwt_token['username'])
            # delete file from DB and file storage
            FileUpload.objects.get(file_uploaded = serializer.data['file_uploaded'][7:]).delete()
            if os.path.exists(file_path):
                os.remove(file_path)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                
@api_view(['POST'])
def download_file(request):
    file=request.data['file_name']
    private_key=request.data['private_key']
    jwt_token=request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    jwt_token=jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
    '''
    1. Query the file data model for username=username and filename=filename
    2. Get horcruxes from different places and place them in media/splits folder
    '''
    if(file):
        filepath=r'\media\files'+"\\"
        filepath=os.getcwd()+filepath+file
        print("filepath",filepath)
        decrypt(filepath, os.getcwd()+'\media\splits',private_key, jwt_token['username'])
        with open(filepath, "rb") as file:
            print("hello")
            response = HttpResponse(file)
            filename = "1-1-intro.pdf"
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
            print(type(response))
            return response


     