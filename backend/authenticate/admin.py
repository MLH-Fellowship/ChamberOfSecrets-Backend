from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin  

from .models import CustomUser

# Register your models here.
class CustomUserAdmin(ModelAdmin):
    model = CustomUser
    list_display = ['user_id', 'email', 'username', 'public_key', 'auth_per_upload']
    list_editable = ['auth_per_upload']

admin.site.register(CustomUser, CustomUserAdmin)