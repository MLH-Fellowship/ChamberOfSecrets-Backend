from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from .models import UserInfo
from .ENV import client_config

# visit https://developers.google.com/drive/api/v3/about-auth for more scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def check_auth_token(user):
    """Checks if the user oauth token is already stored in the database.
    Args:
        user: Username of the user
    Returns:
        Bool: True, if the token exists, False otherwise.
    """
    user_info = UserInfo.objects.get(username=user)
    if user_info.gdrive_token == None:
        return False


def google_oauth_flow():
    """Sets up flow for user auth via Google OAuth
    Returns:
        flow: Google OAuth flow
        redirect_url: The URL where the user has to go to in order to verify themselves
    """
    flow = Flow.from_client_config(client_config, SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')  
    auth_url, _ = flow.authorization_url(prompt='consent')
    return auth_url


def get_auth_token(code):
    """Veryfies the authorization code and generates access token for the user
    Args:
        flow: google_auth_oauthlib.flow.Flow object
        code: Authorization code sent by the user
    Returns:
        access_token: Access token for the user
    """
    flow = Flow.from_client_config(client_config, SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
    flow.fetch_token(code=code)
    access_token = flow.credentials
    return access_token.to_json() 


def generate_token_from_db(user):
    """Fetches the token string from the db and regenerates access token
    Args:
        user: Username of the user
    Returns:
        creds: Access token for the user's Google Drive
    """
    user_info = UserInfo.objects.get(username=user)
    creds = Credentials.from_authorized_user_info(json.loads(user_info.gdrive_token), scopes=SCOPES)
    
    # if credentials have expired, refresh them
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        user_info.gdrive_token = creds.to_json()
        user_info.save()
    return creds



