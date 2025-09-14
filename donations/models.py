from django.db import models
from django.utils import timezone

class Donor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_id = models.CharField(max_length=255, blank=True, null=True)
    flutterwave_payment_id = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # Add this field
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - ${self.amount}"
