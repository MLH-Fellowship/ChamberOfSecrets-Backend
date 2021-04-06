from django.contrib import admin
from django.contrib.admin import ModelAdmin  

from .models import FileData, FileUpload

# Register your models here.

# registering the FileData model that stores users' uploaded file records
class FileDataAdmin(ModelAdmin):
    model = FileData
    list_display = ['username', 'file_id', 'file_name', 'upload_date', 'split_1', 'split_2', 'split_3']  


# registering the FileUpload model that temporarily stored users' uploaded files 
class FileUploadAdmin(ModelAdmin):
    model = FileUpload
    list_display = ['username', 'file_uploaded',] 


admin.site.register(FileData, FileDataAdmin)
admin.site.register(FileUpload, FileUploadAdmin)



