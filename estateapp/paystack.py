import requests

from django.conf import settings

def verify_payment(reference, amount=None):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['data']['status'] == 'success':
            if amount and data['data']['amount'] != amount * 100:
                return False
            return True
    return False