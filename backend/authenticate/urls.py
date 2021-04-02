from django.urls import path
from .views import current_user, UserList, get_gauth_url

# token auth module
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('current_user/', current_user),  # api to verify current user
    path('signup/', UserList.as_view()),  # api for sign up auth
    path('login/', obtain_jwt_token),  # api for login auth
    # path('get-gauth-url/', get_gauth_url),  # api for getting gauth url
]