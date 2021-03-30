from django.db import models

import sys
sys.path.append("..") # Adds higher directory to python modules path.

from authenticate.models import UserInfo
# Create your models here.

# Django model to store horcrux info
class FileData(models.Model):
    user_id = models.ForeignKey(UserInfo, to_field="user_id", on_delete=models.CASCADE)
    file_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=1024)
    split_1 = models.URLField()
    split_2 = models.URLField()
    split_3 = models.URLField()

    class Meta:
        ordering = ['file_id']
        unique_together = [['user_id', 'file_id']]

# django model for temp file storage
class FileUpload(models.Model):
    file_uploaded = models.FileField(upload_to="files/")