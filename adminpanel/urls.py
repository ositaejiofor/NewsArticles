# adminpanel/urls.py
from django.urls import path
from . import views  # make sure views.py exists

urlpatterns = [
    path('', views.index, name='adminpanel-index'),  # placeholder view
]
