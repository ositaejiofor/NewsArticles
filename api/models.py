from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # or CustomUser if you imported directly
        on_delete=models.CASCADE,
        related_name="articles"     # 👈 add this
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
