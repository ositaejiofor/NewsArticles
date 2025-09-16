"""
URL configuration for newsportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Core views
from core import views as core_views

# Sitemap
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import ArticleSitemap, CategorySitemap, UserSitemap

# Define all sitemaps
sitemaps = {
    "articles": ArticleSitemap,
    "categories": CategorySitemap,
    "users": UserSitemap,
}

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Core pages
    path('', include('core.urls')),
    path('blog/', include('blog.urls')),
    path('comments/', include('comments.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('composer_app/', include('composer_app.urls')),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('donations/', include("donations.urls")),

    # API & search
    path('api/', include('api.urls')),
    path("search/", include("search.urls", namespace="search")),

    # Custom admin panel
    path('adminpanel/', include('adminpanel.urls')),

    # CKEditor
    path("ckeditor5/", include('django_ckeditor_5.urls')),


    # Legal pages
    path("privacy-policy/", core_views.privacy_policy, name="privacy_policy"),
    path("terms-of-service/", core_views.terms_of_service, name="terms_of_service"),
    path("disclaimer/", core_views.disclaimer, name="disclaimer"),

    # Sitemap
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

# Serve media files in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
