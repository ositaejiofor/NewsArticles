from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # Fix reverse accessor clashes with groups and permissions
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True,
        help_text=_("The groups this user belongs to."),
        verbose_name=_("groups"),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",
        blank=True,
        help_text=_("Specific permissions for this user."),
        verbose_name=_("user permissions"),
    )

    def __str__(self):
        return self.get_full_name() or self.email


class Profile(models.Model):
    ROLE_ADMIN = "admin"
    ROLE_FAMILY = "family"
    ROLE_VOLUNTEER = "volunteer"

    ROLE_CHOICES = [
        (ROLE_ADMIN, "Administrator"),
        (ROLE_FAMILY, "Family Member"),
        (ROLE_VOLUNTEER, "Volunteer"),
    ]

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="accounts/profiles/", blank=True, null=True
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_FAMILY)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# 🔹 Signals: automatically create/update Profile when CustomUser is saved
@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Safe signal for auto-creating/updating the Profile.
    Uses get_or_create to avoid errors if migrations are out of sync.
    """
    Profile.objects.get_or_create(user=instance)
