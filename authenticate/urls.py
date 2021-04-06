from django.urls import path
from .views import CurrentUserView, UserSignupView, GetGauthUrlView, SetGauthTokenView, GetDropboxauthUrlView, SetDropBoxTokenView, CheckBackendView

# token auth module
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('check/', CheckBackendView.as_view()),  # check to see if backend is responding
    path('login/', obtain_jwt_token),  # api for login auth
    path('signup/', UserSignupView.as_view()),  # api for sign up auth
    path('current_user/', CurrentUserView.as_view()),  # api to verify current user 
    path('get-gauth-url/', GetGauthUrlView.as_view()),  # api for getting gauth url
    path('set-auth-token/', SetGauthTokenView.as_view()),  # api to exchange gdrive auth code for access token
    path('get-dropbox-auth-url/', GetDropboxauthUrlView.as_view()), # api for getting dropbox auth url
    path('set-dropbox-auth-token/', SetDropBoxTokenView.as_view()) # api to exchange dropbox auth code for access token
]