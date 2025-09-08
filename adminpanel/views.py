# adminpanel/views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("AdminPanel URL works!")  # simple placeholder
