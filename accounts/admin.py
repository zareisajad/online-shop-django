from django.contrib import admin

from .models import User, UserProfile

admin.site.register(User)
admin.site.register(UserProfile)
