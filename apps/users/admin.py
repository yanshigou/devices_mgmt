from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin


class UserProfileAdmin(UserAdmin):
    list_display = ('username', 'mobile')


admin.site.register(UserProfile, UserProfileAdmin)
