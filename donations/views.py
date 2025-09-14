from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Sum
import requests
from .forms import DonationForm
from .models import Donor

FLW_BASE_URL = "https://api.flutterwave.com/v3"


# --------------------------
# Main Donation Page
# --------------------------
def donate(request):
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            donor = form.save(commit=False)
            payment_method = form.cleaned_data.get("payment_method")

            # ---------- STRIPE ----------
            if payment_method == "stripe":
                donor.save()
                return redirect("donate_stripe")  # replace with your Stripe checkout URL

            # ---------- FLUTTERWAVE ----------
            elif payment_method == "flutterwave":
                donor.save()
                tx_ref = f"donation-{donor.id}-{int(donor.amount*100)}"

                payload = {
                    "tx_ref": tx_ref,
                    "amount": str(donor.amount),
                    "currency": "NGN",
                    "redirect_url": request.build_absolute_uri("/donations/flw-success/"),
                    "customer": {
                        "email": donor.email,
                        "name": donor.name
                    },
                    "customizations": {
                        "title": "NewsPortal Donation",
                        "description": "Support NewsPortal with your donation"
                    }
                }

                headers = {
                    "Authorization": f"Bearer {settings.FLW_SECRET_KEY}",
                    "Content-Type": "application/json"
                }

                response = requests.post(f"{FLW_BASE_URL}/payments", json=payload, headers=headers)
                data = response.json()

                if data.get("status") == "success":
                    donor.flutterwave_payment_id = tx_ref
                    donor.save()
                    return redirect(data["data"]["link"])
                else:
                    return render(request, "donations/donate.html", {"form": form, "error": data.get("message")})

            # ---------- MANUAL / BANK ----------
            else:
                donor.is_verified = False
                donor.save()
                message = (
                    "Thank you for choosing manual payment. "
                    "Your donation will be verified once received and displayed on the donor wall."
                )
                return render(request, "donations/donate.html", {"form": DonationForm(), "success": message})

    else:
        form = DonationForm()

    return render(request, "donations/donate.html", {"form": form})


# --------------------------
# Flutterwave Success Callback
# --------------------------
def flw_success(request):
    tx_ref = request.GET.get("tx_ref")
    if not tx_ref:
        return render(request, 'donations/flw_success.html')

    headers = {"Authorization": f"Bearer {settings.FLW_SECRET_KEY}"}
    resp = requests.get(f"{FLW_BASE_URL}/transactions/verify_by_tx_ref?tx_ref={tx_ref}", headers=headers)
    data = resp.json()

    donor = Donor.objects.filter(flutterwave_payment_id=tx_ref).first()
    if donor and data.get("status") == "success" and data["data"]["status"] == "successful":
        donor.is_verified = True
        donor.save()

    return render(request, "donations/success.html")


# --------------------------
# Donor Wall
# --------------------------
def donors(request):
    verified_donors = Donor.objects.filter(is_verified=True).order_by('-created_at')
    total_amount = verified_donors.aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'donations/donors.html', {
        'donors': verified_donors,
        'total_amount': total_amount,
    })


# --------------------------
# Success / Cancel Pages
# --------------------------
def donation_success(request):
    return render(request, "donations/success.html")


def donation_cancel(request):
    return render(request, "donations/cancel.html")
