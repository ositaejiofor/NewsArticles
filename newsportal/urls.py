"""
URL configuration for newsportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Core app URLs
    path('blog/', include('blog.urls')),
    path('comments/', include('comments.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('composer_app/', include('composer_app.urls')),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    
    path('', include('core.urls')),

    # API URLs
    path('api/', include('api.urls')),
    path("search/", include("search.urls", namespace="search")),

    # Custom admin panel routes
    path('adminpanel/', include('adminpanel.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)