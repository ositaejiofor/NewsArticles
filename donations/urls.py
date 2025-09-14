from django.urls import path
from . import views

app_name = "donations"

urlpatterns = [
    path("donate/", views.donate, name="donate"),                     # Main donation page
    path("donors/", views.donors, name="donors"),                     # Donor wall
    path("success/", views.donation_success, name="donation_success"),# Generic success page
    path("cancel/", views.donation_cancel, name="donation_cancel"),   # Cancel page
    path("flw-success/", views.flw_success, name="flutterwave_success"), # Flutterwave callback
]
