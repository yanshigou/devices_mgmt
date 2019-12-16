from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'mobile')


admin.site.register(UserProfile, UserProfileAdmin)
