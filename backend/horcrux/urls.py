from django.urls import path

from .views import FileUploadViewSet,download_file

urlpatterns = [
    path('upload/', FileUploadViewSet.as_view()),
    path('download/', download_file), 
]