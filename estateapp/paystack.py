import requests
from django.conf import settings

def initialize_payment(user, amount, plan_name):
    """
    Initializes payment on Paystack and returns the payment link.
    """
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "email": user.email,
        "amount": int(amount) * 100,  # Convert amount to kobo
        "metadata": {"plan": plan_name},
        "callback_url": "http://yourdomain.com/payment/verify/",  # Redirect after payment
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()  # Returns Paystack's response
