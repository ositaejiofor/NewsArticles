from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings



class CustomUser(AbstractUser):
    """
    Custom user model using email as the unique login field.
    """
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # required when creating superusers

    def __str__(self):
        return self.get_full_name() or self.email

class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # ✅ points to your CustomUser
        on_delete=models.CASCADE,
        related_name="profile"
    )
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    website = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
