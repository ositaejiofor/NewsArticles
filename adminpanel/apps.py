# adminpanel/apps.py
from django.apps import AppConfig

class AdminpanelConfig(AppConfig):   # class name can match folder (optional)
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adminpanel'  # must match folder name
