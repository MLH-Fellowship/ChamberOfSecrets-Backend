from django.db import models
from ..authenticate.models import CustomUser

# Create your models here.


class FileData(models.Model):
    user_id = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    file_id = models.AutoField(primary_key=True)
    file_name = models.CharField()

    class Meta:
        ordering = ['file_id']
        unique_together = [['user_id', 'file_id']]


class FileParts(models.Model):
    file_id = models.ForeignKey(to=FileData, on_delete=models.CASCADE)
    split_1 = models.URLField()
    split_2 = models.URLField()
    split_3 = models.URLField()