from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("composer/", include("composer_app.api_urls")),
    path("ads/", include("ads.api_urls")),
    path("adminpanel/", include("adminpanel.api_urls")),
]
