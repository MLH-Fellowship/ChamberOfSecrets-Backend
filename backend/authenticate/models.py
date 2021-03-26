from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(blank=False)  
    user_id = models.AutoField(primary_key=True)
    public_key = models.TextField()
    auth_per_upload = models.BooleanField(default=False)

    class Meta:
        managed = False
        ordering = ['user_id']
        unique_together = [['user_id', 'email', 'username']]