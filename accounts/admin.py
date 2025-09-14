from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile


class ProfileInline(admin.StackedInline):
    model = Profile


class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    model = CustomUser
    list_display = ("email", "username", "is_staff", "is_superuser", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active")
    ordering = ("email",)
    search_fields = ("email", "username")
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "is_staff", "is_superuser", "is_active"),
        }),
    )


# Unregister default User admin if it exists
from django.contrib.auth.models import User
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# Register CustomUser with Profile inline
admin.site.register(CustomUser, CustomUserAdmin)
