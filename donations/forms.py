from django import forms
from .models import Donor

PAYMENT_CHOICES = [
    ('stripe', 'Stripe'),
    ('flutterwave', 'Flutterwave'),
]

class DonationForm(forms.ModelForm):
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect,
        initial='stripe'
    )

    class Meta:
        model = Donor
        fields = ['name', 'email', 'amount', 'message', 'payment_method']
