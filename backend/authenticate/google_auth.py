from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from .models import UserInfo
from .ENV import client_config

# visit https://developers.google.com/drive/api/v3/about-auth for more scopes
SCOPES = ['4/1AY0e-g7Vf0HJlqhiUlA1nL9K6oDTScvKIeFW8ScIvJsf5PhJX2MgfhyPdts']


def check_auth_token(user):
    """Checks if the user oauth token is already stored in the database.
    Args:
        user: Username of the user
    Returns:
        Bool: True, if the token exists, False otherwise.
    """
    user = UserInfo.objects.get(username=user)
    if user.gdrive_token == "":
        return False


def google_oauth_flow():
    """Sets up flow for user auth via Google OAuth
    Returns:
        flow: Google OAuth flow
        redirect_url: The URL where the user has to go to in order to verify themselves
    """
    flow = Flow.from_client_config(client_config, SCOPES)  

    auth_url, _ = flow.authorization_url(prompt='consent')
    return flow, auth_url


def get_auth_token(flow, code):
    """Veryfies the authorization code and generates access token for the user
    Args:
        flow: google_auth_oauthlib.flow.Flow object
        code: Authorization code sent by the user
    Returns:
        access_token: Access token for the user
    """
    flow.fetch_token(code=code)
    access_token = flow.credentials
    return access_token.to_json()






