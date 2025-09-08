from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/dashboard_login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

]
