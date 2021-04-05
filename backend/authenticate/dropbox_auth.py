from dropbox import DropboxOAuth2FlowNoRedirect
from .ENV import dropbox_app_key, dropbox_app_secret
from .models import UserInfo 

SCOPES = ['files.content.read', 'files.content.write']

def check_dropbox_auth_token(user):
    """Checks if the user oauth token is already stored in the database.
    Args:
        user: Username of the user
    Returns:
        Bool: True, if the token exists, False otherwise. 
    """
    user_info = UserInfo.objects.get(username=user)
    if user_info.dropbox_token == None:
        return False
    return True


def dropbox_oauth_flow():
    """Sets up flow for user auth via Dropbox OAuth
    Returns:
        redirect_url: The URL where the user has to go to in order to verify themselves
    """
    auth_flow = DropboxOAuth2FlowNoRedirect(dropbox_app_key, consumer_secret=dropbox_app_secret, token_access_type='offline',scope=SCOPES) 
    auth_url = auth_flow.start()
    return auth_url

def get_dropbox_auth_token(code):
    """Veryfies the authorization code and generates access token for the user
    Args:
        code: Authorization code sent by the user
    Returns:
        access_token: Access token for the user
    """
    auth_flow = DropboxOAuth2FlowNoRedirect(dropbox_app_key, consumer_secret=dropbox_app_secret, token_access_type='offline',scope=SCOPES) 
    auth_result = auth_flow.finish(code)
    access_token = auth_result.access_token
    return access_token
     
def generate_dropbox_token_from_db(user):
    """Fetches the token string from the db and regenerates access token
    Args:
        user: Username of the user
    Returns:
        token: Access token for the user's Dropbox
    """
    user_info = UserInfo.objects.get(username=user)
    token = user_info.dropbox_token  
    return token