import os
from celery import Celery

# Django sozlamalarini to'g'ri import qilish
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('qabul', broker='redis://localhost:6379/0')

@app.task
def process_payment_task(payment_id):
    from payments.models import Payment
    import requests

    payment = Payment.objects.get(id=payment_id)
    provider = payment.provider
    amount = payment.amount

    # API chaqirish
    if provider == "Click":
        response = requests.post("https://click.uz/api/payment", data={"amount": amount})
    elif provider == "Payme":
        response = requests.post("https://payme.uz/api/payment", data={"amount": amount})

    if response.status_code == 200:
        payment.status = "success"
    else:
        payment.status = "failed"

    payment.save()
