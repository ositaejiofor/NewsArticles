# core/urls.py
from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.sitemaps.views import sitemap   # <-- import sitemap
from . import views
from blog.sitemaps import ArticleSitemap           # <-- import your sitemap class

app_name = "core"

# Define your sitemaps dictionary
sitemaps = {
    "articles": ArticleSitemap,
}

urlpatterns = [
    path("", views.home, name="home"),       
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("logout/", auth_views.LogoutView.as_view(next_page="core:home"), name="logout"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),  # works now
]
