from django.urls import path

from .views import FileUploadViewSet, UserFileView

urlpatterns = [
    path('upload/', FileUploadViewSet.as_view()), 
    path('get-files/', UserFileView.as_view()),
]