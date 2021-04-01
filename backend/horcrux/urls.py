from django.urls import path

from .views import FileUploadViewSet, UserFileView, download_file

urlpatterns = [
    path('upload/', FileUploadViewSet.as_view()), 
    path('get-files/', UserFileView.as_view()),
    path('download/', download_file),
]