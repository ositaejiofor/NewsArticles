# comments/urls.py
from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    # Public
    path("", views.comments_home, name="comments_home"),
    
    # Comment CRUD (AJAX)
    path("add/", views.add_comment, name="add_comment"),                  # Add top-level comment
    path("reply/<int:comment_id>/", views.reply_comment, name="reply_comment"),  # Reply to a specific comment
    path("edit/", views.edit_comment, name="edit_comment"),               # Edit own comment
    path("toggle-like/", views.toggle_like, name="toggle_like"),          # Like/unlike

    # Notifications
    path("notifications/", views.check_notifications, name="check_notifications"),

    # Staff moderation
    path("pending/", views.pending_comments, name="pending_comments"),
    path("update-status/", views.update_comment_status, name="update_comment_status"),
]
