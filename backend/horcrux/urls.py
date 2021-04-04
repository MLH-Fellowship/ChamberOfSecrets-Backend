from django.urls import path

from .views import FileUploadView, UserFileView, DownloadFileView

urlpatterns = [
    path('upload/', FileUploadView.as_view()), 
    path('get-files/', UserFileView.as_view()),
    path('download/', DownloadFileView.as_view()),  
]