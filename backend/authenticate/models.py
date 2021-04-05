from django.db import models
from django.contrib.auth.models import User  

# Create your models here.

# custom UserInfo model that stores some extra info for the user
class UserInfo(models.Model):
    username = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE, unique=True)
    public_key = models.TextField()
    auth_per_upload = models.BooleanField(default=False)
    gdrive_token = models.TextField(blank=True) 
    dropbox_token = models.TextField(blank=True)