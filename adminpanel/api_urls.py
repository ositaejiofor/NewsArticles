from django.urls import path
from . import api_views
from . import views


urlpatterns = [
    path('', views.index, name='adminpanel-api-index'),
    path("users/", api_views.UserListCreateAPIView.as_view(), name="api_users"),
    path("users/<int:pk>/", api_views.UserRetrieveUpdateDestroyAPIView.as_view(), name="api_user_detail"),
    path("users/<int:pk>/reset-password/", api_views.UserPasswordResetAPIView.as_view(), name="api_user_reset_password"),
]
