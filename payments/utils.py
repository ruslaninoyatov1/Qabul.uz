import requests
from django.conf import settings

def create_payme_payment(amount, order_id):
    headers = {
        'Authorization': f"Bearer {settings.PAYME_API_KEY}",
    }
    data = {
        'amount': amount,
        'order_id': order_id,
        'currency': 'UZS',  # UZS so'm uchun
        # Boshqa kerakli parametrlar
    }
    response = requests.post(settings.PAYME_API_URL, json=data, headers=headers)
    return response.json()
