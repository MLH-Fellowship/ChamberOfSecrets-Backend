from django.urls import path
from .views import CurrentUserView, UserListView, GetGauthUrlView, SetGauthTokenView

# token auth module
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('current_user/', CurrentUserView.as_view()),  # api to verify current user 
    path('signup/', UserListView.as_view()),  # api for sign up auth
    path('login/', obtain_jwt_token),  # api for login auth
    path('get-gauth-url/', GetGauthUrlView.as_view()),  # api for getting gauth url
    path('set-auth-token/', SetGauthTokenView.as_view()),  # api to exchange auth code for access token
]