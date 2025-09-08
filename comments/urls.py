from django.urls import path
from . import views

app_name = 'comments'  # namespace for reverse() and {% url %}

urlpatterns = [
    # Default comments page
    path('', views.comments_home, name='comments_home'),

    # Add a comment to a post
    path('add/<int:post_id>/', views.add_comment, name='add_comment'),

    # Pending comments (admin view)
    path('pending/', views.pending_comments, name='pending_comments'),

    # Update comment status (approve/reject)
    path('update-status/', views.update_comment_status, name='update_comment_status'),

    # Toggle like/unlike for a comment
    path('toggle-like/', views.toggle_like, name='toggle_like'),
]
