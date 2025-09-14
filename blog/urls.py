from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # Homepage (can list all articles or handle search)
    path("", views.home, name="home"),

    path("articles/", views.article_list, name="article_list"),

    path("articles/<slug:slug>/", views.article_detail, name="article_detail"),

    # List all articles (paginated)
    path("articles/", views.article_list, name="article_list"),

    # Article detail by slug
    path("article/<slug:slug>/", views.article_detail, name="article_detail"),

    # Category detail by slug (paginated list of articles in that category)
    path("category/<slug:slug>/", views.category_detail, name="category"),

    # Optional: Filter articles by category (can reuse category_detail if desired)
    path("category/<slug:slug>/articles/", views.posts_by_category, name="posts_by_category"),

    path("<slug:slug>/", views.article_detail, name="article_detail"),  # ✅ correct name
    path("articles/<slug:slug>/", views.article_detail, name="article_detail"),

    path("<slug:slug>/", views.article_detail, name="article_detail"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),

]
