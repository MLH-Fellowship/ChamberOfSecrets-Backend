from rest_framework import serializers

from .models import FileUpload, FileData


# serializer for FileUpload model
class FileUploadSerializer(serializers.ModelSerializer):
    file_uploaded = serializers.FileField()

    class Meta:
        model = FileUpload
        fields = ['file_uploaded']  



# serializer for FileData model
class FileDataSerializer(serializers.Serializer):
    file_name = serializers.CharField(max_length=1024)
    split_1 = serializers.CharField()
    split_2 = serializers.CharField()
    split_3 = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new FileData instance, given the validated data.
        """
        return self.Meta.model.objects.create(**validated_data)

    class Meta:
        model = FileData
        fields = ('file_name', 'split_1', 'split_2','split_3')