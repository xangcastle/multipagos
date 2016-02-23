from django.contrib import admin
from .models import *


class profile_admin(admin.ModelAdmin):
    list_display = ('user', 'celular')

admin.site.register(UserProfile, profile_admin)
