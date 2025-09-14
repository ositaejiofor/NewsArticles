from django.db import models
from django.conf import settings


class DashboardPreference(models.Model):
    CHART_TYPES = [
        ("bar", "Bar Chart"),
        ("stacked", "Stacked Bar Chart"),
    ]

    TIME_RANGES = [
        ("month", "Per Month"),
        ("year", "Per Year"),
        ("all", "All Time"),
        ("custom", "Custom Range"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="dashboard_preference"
    )
    chart_type = models.CharField(
        max_length=20,
        choices=CHART_TYPES,
        default="bar"
    )
    cumulative = models.BooleanField(default=False)
    time_range = models.CharField(
        max_length=20,
        choices=TIME_RANGES,
        default="month"
    )
    custom_start = models.DateField(null=True, blank=True)
    custom_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Dashboard Preferences"
