from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from .models import UserInfo


# serializer for User model
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username',)

# serializer for User model
class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    # generates JWT token
    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    # creates model instance 
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password')

# serializer for UserInfo model
class UserInfoSerializer(serializers.Serializer):
    public_key = serializers.CharField()
    auth_per_upload = serializers.BooleanField()
    gdrive_token = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new UserInfo instance, given the validated data.
        """
        return self.Meta.model.objects.create(**validated_data)

    class Meta:
        model = UserInfo
        fields = ('public_key', 'auth_per_upload', 'gdrive_token')