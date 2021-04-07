import io
import os
import jwt
import json
from datetime import datetime
import dropbox

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.viewsets import ViewSet
from rest_framework import status as s
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import FileUpload, FileData 
from .encryption_decryption.combined import encrypt, decrypt
from .serializers import FileUploadSerializer, FileDataSerializer, UserFileSerializer
from .utils import get_user_from_jwt, get_drive_services 

from authenticate.google_auth import check_google_auth_token
from authenticate.dropbox_auth import check_dropbox_auth_token

from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload 

# global vars
splits_dir = os.path.join(os.getcwd(), 'media', 'splits')  # directory where horcruxes are temp stored
media_dir = os.path.join(os.getcwd(), "media", "files")  # dir where files are temp stored 


class FileUploadView(APIView):
    """
    POST API that lets user upload a file, divides it into horcruxes 
    and uploads it on various storage platforms 
    """
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request):
        return Response("POST API")


    def post(self, request):
        
        # getting username and User model object from JWT token
        username, user = get_user_from_jwt(request)
        
        try:
            request.data['file_uploaded'].name = request.data['file_uploaded'].name
            file_name = request.data['file_uploaded'].name
            files = FileUpload.objects.all().filter(username=user)
            if len(files) > 0: 
                for file in files:
                    file.delete() 
        except:
            pass
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(username=user)

            file_path = os.getcwd() + serializer.data['file_uploaded'].replace('/', '\\')  # getting file path

            # check if an entry with the same name already exists 
            try:
                file_exists = FileData.objects.get(username=user, file_name=file_name)
                unique_id = str((datetime.now() - file_exists.upload_date.replace(tzinfo=None)).seconds) + "_" 
                file_name = unique_id + file_name
            except ObjectDoesNotExist:
                pass
            

            
                # file encryption and splitting
            encrypt(file_path, splits_dir, request.data['private_key'], username, file_name)
        
            # delete file from DB and file storage
            FileUpload.objects.get(username=user, file_uploaded = serializer.data['file_uploaded'][7:]).delete()  
                # for file in os.listdir(media_dir):
                #     os.remove(os.path.join(media_dir, file))
                # return Response({"message": "You entered an invalid private key!"}, status=s.HTTP_400_BAD_REQUEST) 

            # delete file from DB and file storage
            FileUpload.objects.get(username=user, file_uploaded = serializer.data['file_uploaded'][7:]).delete()  
            for file in os.listdir(media_dir): 
                os.remove(os.path.join(media_dir, file))  

            # uploading on google drive
            if check_google_auth_token(user=username) and check_dropbox_auth_token(user=username):
                # generating drive services
                g_service, d_service = get_drive_services(username)  
                # getting files   
                files = os.listdir(splits_dir)
                files.sort()
                # uploading on google drive
                uploaded_file = g_service.files().create(media_body=MediaFileUpload(os.path.join(splits_dir, files[0]), 
                                                                                  mimetype='*/*'), fields='id').execute()
                split_1 = uploaded_file.get('id')
                uploaded_file = g_service.files().create(media_body=MediaFileUpload(os.path.join(splits_dir, files[2]), 
                                                                                  mimetype='*/*'), fields='id').execute()
                split_3 = uploaded_file.get('id')
                uploaded_file = None
                # uploading on dropbox
                split_2 = d_location = f"/DigiCrux/{str((datetime.now() - datetime(2001, 11, 4)).seconds)}"  # time in seconds from release of first Harry Potter movie
                with open(os.path.join(splits_dir, files[1]), "rb") as f: 
                    d_service.files_upload(f.read(), d_location, mode=dropbox.files.WriteMode.overwrite)
                # removing the splits
                for file in files:
                    os.remove(os.path.join(splits_dir, file)) 
            else:
                # removing the splits
                for file in files:
                    os.remove(os.path.join(splits_dir, file)) 
                return Response({"message": "Can't access storage. Upload failed!"}, status=s.HTTP_409_CONFLICT)

            # creating a log in FileData db table 
            file_data = {'file_name':file_name, 'split_1':split_1, 'split_2':split_2,'split_3':split_3}
            serializer_filedata = FileDataSerializer(data=file_data)
            if serializer_filedata.is_valid():
                serializer_filedata.save(username=user)  # creates FileData instance
            return Response({"file_uploaded": file_name}, status=s.HTTP_201_CREATED) 
        return Response(serializer.errors, status=s.HTTP_400_BAD_REQUEST)


class DownloadFileView(APIView):
    """
    Downloads the horcurxes from user's file storages then combines+decrypts 
    the horcruxes back into the original file which is sent back to the user.
    """
                
    def post(self, request): 
        file_name = request.data['file_name']
        private_key = request.data['private_key']
        # getting username and User model object from JWT token
        username, user = get_user_from_jwt(request)
        
        try:
            file_record = FileData.objects.get(username=user, file_name=file_name)
            split_1 = file_record.split_1  # gdrive file id
            split_2 = file_record.split_2  # dropbox file 
            split_3 = file_record.split_3  # gdrive file id 
        except ObjectDoesNotExist:
            return Response({"message": "File not found!"}, status=s.HTTP_404_NOT_FOUND)
        # downloading the splits
        if check_google_auth_token(user=username) and check_dropbox_auth_token(user=username):
            # generating drive services
            g_service, d_service = get_drive_services(username) 
            # downloading from dropbox
            d_service.files_download_to_file(os.path.join(splits_dir, f"{file_name}02"), split_2)
            # downloading from gdrive
            for i, split in zip((1, 3), (split_1, split_3)):
                request = g_service.files().get_media(fileId=split)
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                fh.seek(0)
                with open(os.path.join(splits_dir, f"{file_name}0{i}"), "wb") as f:  
                    f.write(fh.read())
            # join and decrypt the file
            if(file_name):  
                filepath = os.path.join(os.getcwd(), "media", "files", file_name)
                try:
                    decrypt(filepath, splits_dir, private_key, username)
                except:
                    # deleting the splits from storage
                    for file in os.listdir(splits_dir):
                        os.remove(os.path.join(splits_dir, file))
                    return Response({"message": "You entered an invalid private key!"}, status=s.HTTP_400_BAD_REQUEST) 
                with open(filepath, "rb") as f:
                    response = HttpResponse(f)
                    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
                    # deleting the splits from storage
                    for file in os.listdir(splits_dir):
                        os.remove(os.path.join(splits_dir, file))
                    # deleting file storage
                    for file in os.listdir(media_dir):
                        os.remove(os.path.join(media_dir, file)) 
                    return response
        return Response({"message": "Can't access storage. Download failed!"}, status=s.HTTP_409_CONFLICT) 



class FileDeleteView(APIView):
    """
    Deletes file record from the database, along with the horcruxes from the file storages.
    """

    def post(self, request):
        # getting username and User model object from JWT token
        username, user = get_user_from_jwt(request)
        # check if the file record exists in the database
        file_name = request.data['file_name'] 
        try: 
            file_record = FileData.objects.get(username=user, file_name=file_name)
            print(file_record)
        except ObjectDoesNotExist:
            return Response({"message": "File not found!"}, status=s.HTTP_404_NOT_FOUND)
            pass
        # downloading the splits
        if check_google_auth_token(user=username) and check_dropbox_auth_token(user=username):
            # generating drive services
            g_service, d_service = get_drive_services(username) 
            # deleting horcruxes on gdrive
            try:
                g_service.files().delete(fileId=file_record.split_1).execute()
                g_service.files().delete(fileId=file_record.split_3).execute()
            except:
                return Response({"message": "Could not delete from Google Drive"}, status=s.HTTP_417_EXPECTATION_FAILED)
            # deleting horcrux on dropbox 
            try:
                d_service.files_delete_v2(file_record.split_2)
            except:
                return Response({"message": "Could not delete from Dropbox"}, status=s.HTTP_417_EXPECTATION_FAILED)
            # deleting record from database
            file_record.delete() 

            return Response({"message": "File deleted successfully"}, status=s.HTTP_200_OK)
            

   
class UserFileView(APIView):
    """
    GET api that fetches the list of files owned by the user.
    """
    serializer_class = UserFileSerializer
    
    def list(self, request):
        return Response("GET API")
    
    def get(self, request):
        # getting username and User model object from JWT token
        username, user = get_user_from_jwt(request)
        user_files = FileData.objects.filter(username=user)
        serializer = UserFileSerializer(user_files, many=True) 

        return Response(serializer.data) 
 




     
