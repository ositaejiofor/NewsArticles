from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),       # /
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("logout/", auth_views.LogoutView.as_view(next_page="core:home"), name="logout"),

]
