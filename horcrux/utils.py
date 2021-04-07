# helper methods for view.py
import os
import jwt

from django.conf import settings
from django.contrib.auth.models import User

from authenticate.google_auth import generate_google_token_from_db
from authenticate.dropbox_auth import generate_dropbox_token_from_db, dropbox_app_key  

import dropbox 
from googleapiclient.discovery import build


def get_user_from_jwt(request):
    """Method to fetch username and User model object from JWT token.
    Args-
        request: HTTP request received from client.
    Returns-
        username::str: Username decoded from the JWT token.
        user::Django User model: User model object associated with the username  
    """
    jwt_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]  
    jwt_token = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
    username = jwt_token['username']
    user = User.objects.get(username=username)
    return username, user 

def get_drive_services(username):
    """Method to generate google drive and dropbox services using credentials from DB.
    Args-
        username::str: Username of the user
    Returns-
        g_service: Google drive service for interacting with user's GDrive
        d_service: Dropbox service to interact with user's Dropbox
    """
    g_creds = generate_google_token_from_db(user=username)  # google drive creds
    d_creds = generate_dropbox_token_from_db(user=username)  # dropbox creds
    # building google drive service
    g_service = build('drive', 'v3', credentials=g_creds)
    # building dropbox service 
    d_service = dropbox.Dropbox(app_key=dropbox_app_key, **d_creds)
    d_service.check_and_refresh_access_token()
    return g_service, d_service