from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    model = CustomUser

# Unregister default User admin if it exists
from django.contrib.auth.models import User
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# Register CustomUser with inline
admin.site.register(CustomUser, CustomUserAdmin)
