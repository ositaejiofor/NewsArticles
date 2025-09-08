from django.urls import path
from . import api_views

urlpatterns = [
    path("ads/", api_views.AdListCreateAPIView.as_view(), name="api_ads_list"),
    path("ads/<int:pk>/", api_views.AdDetailAPIView.as_view(), name="api_ads_detail"),
]
