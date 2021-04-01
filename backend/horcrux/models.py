from django.db import models

import sys
sys.path.append("..") # Adds higher directory to python modules path.

from django.contrib.auth.models import User 
# Create your models here.

# Django model to store horcrux info
class FileData(models.Model):
    username = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE)
    file_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=1024)
    upload_date = models.DateTimeField(auto_now=True)
    upload_file_name = models.CharField(max_length=1030)
    split_1 = models.TextField()
    split_2 = models.TextField()
    split_3 = models.TextField()

    class Meta:
        ordering = ['file_id']
        unique_together = [['username', 'file_id']]

# django model for temp file storage
class FileUpload(models.Model):
    file_uploaded = models.FileField(upload_to="files/")