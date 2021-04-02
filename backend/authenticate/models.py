from django.db import models
from django.contrib.auth.models import User  

# Create your models here.
class UserInfo(models.Model):
    username = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE, unique=True)
    public_key = models.TextField()
    auth_per_upload = models.BooleanField(default=False) 