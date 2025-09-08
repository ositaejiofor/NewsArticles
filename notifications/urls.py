from django.urls import path
from . import views

app_name = 'notifications'



urlpatterns = [
    path('all/', views.all_notifications, name='all'),
    path('read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
]
