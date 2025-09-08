from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.home, name="home"),  # Homepage + search
    path("post/<int:pk>/", views.post_detail, name="post_detail"),  # Post detail
    path("category/<slug:slug>/", views.posts_by_category, name="posts_by_category"),

]
