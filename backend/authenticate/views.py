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

# Create your views here.

@api_view(['GET'])
def current_user(request):
    """
    Checks for and determines the current user by their token, and return their data
    """
    
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user via sign-up.
    
    JSON format:

    {
        "username":"",
        "password":"",
        "public_key":"",
        "auth_per_upload":"True/False"
    }

    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer_user = UserSerializerWithToken(data=request.data)  # seralizer for User model 
        serializer_userinfo = UserInfoSerializer(data=request.data)  # serializer for UserInfo model
        
        if serializer_user.is_valid():
            serializer_user.save()  # saves the user model
            #Response(serializer_user.data, status=status.HTTP_201_CREATED)  # TODO: remove this line and uncomment the bottom part later
            if serializer_userinfo.is_valid():
                user = User.objects.get(username=request.data['username'])
                serializer_userinfo.save(username=user)  # save userinfo model
                serializer_user_data = serializer_user.data  # creating a copy of serializer.data

                # generating private key jwt
                private_key_payload = {'private': 'ThisIsAPrivateKey'}  # replace private key value with the generated one
                private = jwt.encode(private_key_payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
                serializer_user_data['private'] = private

                return Response(serializer_user_data, status=status.HTTP_201_CREATED)  # returns response with JWT token
        return Response(serializer_user.errors, status=status.HTTP_400_BAD_REQUEST)  # returns response error code