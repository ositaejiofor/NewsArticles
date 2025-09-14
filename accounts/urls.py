from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # Auth
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

 # Profile AJAX data
    path('profile/analytics-data/', views.profile_analytics_data, name='profile_analytics_data'),

    # Other profile URLs
    path('profile/', views.profile_dashboard, name='profile_dashboard'),
    path('profile/view/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
