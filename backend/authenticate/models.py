from django.db import models
from django.contrib.auth.models import User  

# Create your models here.
class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=256)
    public_key = models.TextField()
    auth_per_upload = models.BooleanField(default=False)

    class Meta:
        unique_together = [['user_id', 'username']]