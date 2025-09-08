from django.urls import path
from . import api_views
from .api_views import ResetPasswordAPIView


urlpatterns = [
    path("articles/", api_views.ArticleListCreateAPIView.as_view(), name="api_article_list"),
    path("articles/<slug:slug>/", api_views.ArticleDetailAPIView.as_view(), name="api_article_detail"),
    path("reset-password/", ResetPasswordAPIView.as_view(), name="reset-password"),

]
