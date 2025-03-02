import os
from celery import Celery
from celery import shared_task
from django.contrib.auth import get_user_model
from .utils import send_email_notification, send_telegram_notification, save_user_chat_id

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


User = get_user_model()


@shared_task
def send_email_async(user_id, subject, message):

    user = User.objects.get(id=user_id)
    send_email_notification(user, subject, message)


@shared_task
def send_telegram_async(user_id, message):

    user = User.objects.get(id=user_id)
    send_telegram_notification(user, message)


@shared_task
def save_chat_id_task(user_id, chat_id):

    save_user_chat_id(user_id, chat_id)

