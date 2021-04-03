from django.urls import path

from .views import FileUploadViewSet, UserFileView, DownloadFile

urlpatterns = [
    path('upload/', FileUploadViewSet.as_view()), 
    path('get-files/', UserFileView.as_view()),
    path('download/', DownloadFile.as_view()), 
]