from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    public_key = models.TextField()
    auth_per_upload = models.BooleanField(default=False)

    class Meta:
        managed = False
        unique_together = [['user_id', 'email', 'username']]