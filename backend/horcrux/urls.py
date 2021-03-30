from django.urls import path

from .views import FileUploadViewSet

urlpatterns = [
    path('upload/', FileUploadViewSet.as_view()), 
]