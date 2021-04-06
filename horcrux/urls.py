from django.urls import path

from .views import FileUploadView, UserFileView, DownloadFileView, FileDeleteView

# url mapping for the horcrux app views
urlpatterns = [
    path('upload/', FileUploadView.as_view()),  # endpoint to upload files 
    path('get-files/', UserFileView.as_view()),  # endpoint to get all the user's files
    path('download/', DownloadFileView.as_view()),  # endpoint for downloading a file
    path('delete/', FileDeleteView.as_view()),  # endpoint to delete a file
]