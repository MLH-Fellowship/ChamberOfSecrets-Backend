import io
import os
import jwt
import json
from datetime import datetime
import dropbox

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.viewsets import ViewSet
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser

from .models import FileUpload, FileData 
from .encryption_decryption.combined import encrypt, decrypt
from .serializers import FileUploadSerializer, FileDataSerializer, UserFileSerializer

from authenticate.google_auth import check_google_auth_token, generate_google_token_from_db
from authenticate.dropbox_auth import check_dropbox_auth_token, generate_dropbox_token_from_db
from authenticate.models import UserInfo 

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload



# POST API that lets user upload a file, divides it into horcruxes and uploads it on various storage platforms 
class FileUploadView(APIView):
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request):
        return Response("POST API")


    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            file_path = os.getcwd() + serializer.data['file_uploaded'].replace('/', '\\')  # getting file path
            jwt_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]  
            jwt_token = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
            username = jwt_token['username']

            # check if an entry with the same name already exists
            user = User.objects.get(username=username) 
            file_name = request.data['file_uploaded'].name
            try:
                file_exists = FileData.objects.get(username=user, file_name=file_name)
                unique_id = str((datetime.now() - file_exists.upload_date.replace(tzinfo=None)).seconds) + "_" 
                file_name = unique_id + file_name
            except ObjectDoesNotExist:
                pass
            
            # file encryption and splitting
            encrypt(file_path, os.getcwd()+'\media\splits', request.data['private_key'], username, file_name)
            # delete file from DB and file storage
            FileUpload.objects.get(file_uploaded = serializer.data['file_uploaded'][7:]).delete()
            media_files = os.getcwd()+ r"\media\files"  
            for file in os.listdir(media_files):
                os.remove(os.path.join(media_files, file))

            # uploading on google drive
            if check_google_auth_token(user=username) and check_dropbox_auth_token(user=username):
                g_creds = generate_google_token_from_db(user=username)  # google drive creds
                d_creds = generate_dropbox_token_from_db(user=username)  # dropbox creds
                # building google drive service
                g_service = build('drive', 'v3', credentials=g_creds)
                # building dropbox service
                d_service = dropbox.Dropbox(d_creds)
                # getting file dir
                file_dir = os.getcwd() + '\media\splits'   
                files = os.listdir(file_dir)
                files.sort()
                # uploading on google drive
                uploaded_file = g_service.files().create(media_body=MediaFileUpload(os.path.join(file_dir, files[0]), 
                                                                                  mimetype='*/*'), fields='id').execute()
                split_1 = uploaded_file.get('id')
                uploaded_file = g_service.files().create(media_body=MediaFileUpload(os.path.join(file_dir, files[2]), 
                                                                                  mimetype='*/*'), fields='id').execute()
                split_3 = uploaded_file.get('id')
                uploaded_file = None
                # uploading on dropbox
                split_2 = d_location = f"/DigiCrux/{str((datetime.now() - datetime(2001, 11, 4)).seconds)}"  # time in seconds from release of first Harry Potter movie
                with open(os.path.join(file_dir, files[1]), "rb") as f: 
                    d_service.files_upload(f.read(), d_location, mode=dropbox.files.WriteMode.overwrite)
                # removing the splits
                for file in files:
                    os.remove(os.path.join(file_dir, file)) 
            else:
                return Response(status=status.HTTP_409_CONFLICT)

            # creating a log in FileData db table 
            file_data = {'file_name':file_name, 'split_1':split_1, 'split_2':split_2,'split_3':split_3}
            serializer_filedata = FileDataSerializer(data=file_data)
            if serializer_filedata.is_valid():
                serializer_filedata.save(username=user)  # creates FileData instance
            return Response({"file_uploaded": file_name}, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DownloadFileView(APIView):
    """Downloads the horcurxes from user's file storages then combines+decrypts 
    the horcruxes back into the original file which is sent back to the user.
    """
                
    def post(self, request): 
        file_name = request.data['file_name']
        private_key = request.data['private_key']
        jwt_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        jwt_token = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
        
        # fetching the file record
        username = jwt_token['username']
        user = User.objects.get(username=username)
        try:
            file_record = FileData.objects.get(username=user, file_name=file_name)
            split_1 = file_record.split_1  # gdrive file id
            split_2 = file_record.split_2  # dropbox file 
            split_3 = file_record.split_3  # gdrive file id 
        except ObjectDoesNotExist:
            return Response("File not found!", status=status.HTTP_404_NOT_FOUND)

        # downloading the splits
        if check_google_auth_token(user=username) and check_dropbox_auth_token(user=username):
            g_creds = generate_google_token_from_db(user=username)  # google drive creds
            d_creds = generate_dropbox_token_from_db(user=username)  # dropbox creds
            # building google drive service
            g_service = build('drive', 'v3', credentials=g_creds)
            # building dropbox service 
            d_service = dropbox.Dropbox(d_creds)
            file_dir = os.getcwd() + '\media\splits'  # dir for file downloads
            # downloading from dropbox
            d_service.files_download_to_file(os.path.join(file_dir, f"{file_name}02"), split_2)
            # downloading from gdrive
            for i, split in zip((1, 3), (split_1, split_3)):
                request = g_service.files().get_media(fileId=split)
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                fh.seek(0)
                with open(os.path.join(file_dir, f"{file_name}0{i}"), "wb") as f:  
                    f.write(fh.read())

        # join and decrypt the file
        if(file_name):
            filepath = r"\media\files\\"   
            filepath = os.getcwd() + filepath + file_name
            decrypt(filepath, os.getcwd() + '\media\splits', private_key, username)
            with open(filepath, "rb") as f:
                print("hello")
                response = HttpResponse(f)
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
                # deleting the splits from storage
                for file in os.listdir(file_dir):
                    os.remove(os.path.join(file_dir, file)) 
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




     