import os
import json
from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.viewsets import ViewSet
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from .encryption_decryption.combined import encrypt,decrypt
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import FileUploadSerializer, FileDataSerializer, UserFileSerializer
from .models import FileUpload, FileData 
from django.conf import settings
import jwt



# POST API that lets user upload a file, divides it into horcruxes and uploads it on various storage platforms 
class FileUploadViewSet(APIView):
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request):
        return Response("POST API")


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
            file_name = request.data['file_uploaded'].name
            upload_file_name = serializer.data['file_uploaded'][13:]
            split_1 = 'dummy text'  # Replace w/ url or fileId for the storage platform
            split_2 = 'dummy text'
            split_3 = 'dummy text'
            file_data = {'file_name':file_name, 'upload_file_name': upload_file_name,'split_1':split_1, 'split_2':split_2,'split_3':split_3}
            serializer_filedata = FileDataSerializer(data=file_data)
            if serializer_filedata.is_valid():
                serializer_filedata.save(username=user)  # creates FileData instance

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


# GET api that fetches the list of files owned by the user   
class UserFileView(APIView):
    serializer_class = UserFileSerializer
    
    def list(self, request):
        return Response("GET API")
    
    def get(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]  
        jwt_token = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
        user_files = FileData.objects.filter(username=jwt_token['username'])
        serializer = UserFileSerializer(user_files, many=True)
        return Response(serializer.data)




     