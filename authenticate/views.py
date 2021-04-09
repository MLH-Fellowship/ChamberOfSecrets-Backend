import jwt
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.conf import settings

from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from .serializers import UserSerializer, UserSerializerWithToken, UserInfoSerializer
from .keys import generate_private_key, generate_encrypted_public_key
from .google_auth import google_oauth_flow, get_google_auth_token
from .dropbox_auth import dropbox_oauth_flow, get_dropbox_auth_token
from .models import UserInfo


# Create your views here.

class CheckBackendView(APIView):
    """Test if the backend is responding."""
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response({"message": "It's working!"}, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    """
    Checks for and determines the current user by their token, and return their data
    """
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data) 


class UserSignupView(APIView):
    """
    Create a new user via sign-up.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer_user = UserSerializerWithToken(data=request.data)  # seralizer for User model 
        
        private_key = generate_private_key()
        encrypted_public_key = generate_encrypted_public_key(private_key)
        encrypted_public_key = str(encrypted_public_key, 'utf-8')
        request.data['public_key'] = encrypted_public_key

        serializer_userinfo = UserInfoSerializer(data=request.data)  # serializer for UserInfo model
        
        if serializer_user.is_valid():
            serializer_user.save()  # saves the user model
            if serializer_userinfo.is_valid():
                user = User.objects.get(username=request.data['username'])
                
                # updating firstname and lastname once the user is created
                user.first_name = request.data['firstname']
                user.last_name = request.data['lastname']
                user.save()
                
                # save userinfo model 
                serializer_userinfo.save(username=user)  
                serializer_user_data = serializer_user.data  # creating a copy of serializer.data

                # generating private key jwt
                private_key_payload = {'private': str(private_key,'utf-8')}  # replace private key value with the generated one
                private = jwt.encode(private_key_payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
                serializer_user_data['private'] = private 
                return Response(serializer_user_data, status=status.HTTP_201_CREATED)  # returns response with JWT token
        return Response(serializer_user.errors, status=status.HTTP_400_BAD_REQUEST)  # returns response error code



class GetGauthUrlView(APIView):
    """
    GET API endpoint to fetch the google auth url
    """
    def get(self, request):
        auth_url = google_oauth_flow()
        return Response(auth_url)


class GetDropboxauthUrlView(APIView):
    """
    GET API endpoint to fetch the dropbox auth url
    """
    def get(self, request):
        auth_url = dropbox_oauth_flow()
        return Response(auth_url)



class SetGauthTokenView(APIView):
    """
    POST API endpoint to set the user's Google Drive access token.
    """

    def post(self, request):
        # generating the access token
        try:
            access_token = get_google_auth_token(code=request.data['code'])
        except:
            return Response({"message":"You entered a wrong authentication code."}, status=status.HTTP_400_BAD_REQUEST)
        # saving the access token to the DB
        jwt_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]  
        jwt_token = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
        user_info = UserInfo.objects.get(username=jwt_token['username'])
        user_info.gdrive_token = access_token
        user_info.save()

        return Response({"message": "Drive authentication successful"}, status=status.HTTP_201_CREATED)  

class SetDropBoxTokenView(APIView):
    """
    POST API endpoint to set the user's Dropbox access token.
    """

    def post(self, request):
        # generating the access token
        try:
            token_json = get_dropbox_auth_token(code=request.data['code'])
        except:
            return Response({"message":"You entered a wrong authentication code."}, status=status.HTTP_400_BAD_REQUEST)
        # saving the access token to the DB
        jwt_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]  
        jwt_token = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
        user_info = UserInfo.objects.get(username=jwt_token['username'])
        user_info.dropbox_token = token_json
        user_info.save()

        return Response({"message": "Dropbox authentication successful"}, status=status.HTTP_201_CREATED)