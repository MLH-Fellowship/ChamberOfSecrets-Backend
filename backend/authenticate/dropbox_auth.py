from dropbox import DropboxOAuth2FlowNoRedirect
from .ENV import dropbox_app_key, dropbox_app_secret

SCOPES = ['files.content.read', 'files.content.write']

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
     
