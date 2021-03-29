from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken, UserInfoSerializer


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
        "auth_per_upload":""
    }

    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer_user = UserSerializerWithToken(data=request.data)  # seralizer for User model 
        serializer_userinfo = UserInfoSerializer(data=request.data)  # serializer for UserInfo model
        
        if serializer_user.is_valid():
            serializer_user.save()  # saves the user model
            return Response(serializer_user.data, status=status.HTTP_201_CREATED)  # TODO: remove this line and uncomment the bottom part later
            # if serializer_userinfo.is_valid():
            #     user = User.objects.get(username=request.data['username'])
            #     serializer_userinfo.save(username=user)  # save userinfo model
            #     return Response(serializer_user.data, status=status.HTTP_201_CREATED)  # returns response with JWT token
        return Response(serializer_user.errors, status=status.HTTP_400_BAD_REQUEST)  # returns response error code