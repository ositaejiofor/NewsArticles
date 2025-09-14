# comments/models.py
from django.db import models
from django.conf import settings
from blog.models import Article
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model


class Comment(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )
    content = RichTextField(config_name="default")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name="liked_comments"
    )
    notified = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]  # latest comments first
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        """Display a short preview for admin or debugging."""
        preview = self.content[:50] + ("..." if len(self.content) > 50 else "")
        return f"{self.user} - {preview}"

    def like_count(self):
        return self.likes.count()

    def is_reply(self):
        """Check if this comment is a reply to another comment."""
        return self.parent is not None

    def is_top_level(self):
        """Return True if comment has no parent."""
        return self.parent is None

    def get_depth(self):
        """Return nesting depth for replies (0 = top-level)."""
        depth = 0
        parent = self.parent
        while parent:
            depth += 1
            parent = parent.parent
        return depth

    def children(self):
        """Return immediate child replies (approved only)."""
        return self.replies.filter(status="approved")

    def approved(self):
        """Return True if comment is approved."""
        return self.status == "approved"
