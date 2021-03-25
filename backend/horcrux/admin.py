from django.contrib import admin
from django.contrib.admin import ModelAdmin  

from .models import FileData, FileParts

# Register your models here.

class FileDataAdmin(ModelAdmin):
    model = FileData
    list_display = ['user_id', 'file_id', 'file_name']
    
class FilePartsAdmin(ModelAdmin):
    model = FileParts
    list_display = ['file_id', 'split_1', 'split_2', 'split_3']
    

admin.site.register(FileData, FileDataAdmin)
admin.site.register(FileParts, FilePartsAdmin)



