from rest_framework import serializers

from .models import FileUpload

class FileUploadSerializer(serializers.ModelSerializer):
    file_uploaded = serializers.FileField()

    class Meta:
        model = FileUpload
        fields = ['file_uploaded']  

