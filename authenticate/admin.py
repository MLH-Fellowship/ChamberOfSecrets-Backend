from django.contrib import admin
from django.contrib.admin import ModelAdmin  

from .models import UserInfo

# Register your models here.

class UserInfoAdmin(ModelAdmin):
    model = UserInfo
    list_display = ['username', 'public_key', 'auth_per_upload']
    

admin.site.register(UserInfo, UserInfoAdmin)