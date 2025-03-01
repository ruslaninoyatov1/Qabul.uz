import logging
import requests
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from telegram import Bot
from logs.models import NotificationLog

logger = logging.getLogger("django")
User = get_user_model()

TELEGRAM_BOT_TOKEN = "7408258357:AAF-NDdLcL8g6mhAuc9cU7zHoXOvcV49jAA"
bot = Bot(token=TELEGRAM_BOT_TOKEN)


def send_email_notification(user, subject, message):
    """
    Foydalanuvchiga email xabarnoma yuboradi va logga yozadi.
    """
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
        NotificationLog.objects.create(user=user, notification_type="email", status="sent")
        logger.info(f"Email sent to {user.email}")
    except Exception as e:
        NotificationLog.objects.create(user=user, notification_type="email", status="failed", error_message=str(e))
        logger.error(f"Email failed for {user.email}: {e}")


def send_telegram_notification(user, message):
    """
    Foydalanuvchiga Telegram xabar yuborish.
    """
    chat_id = getattr(user, "chat_id", None)
    if not chat_id:
        logger.warning(f"Telegram chat_id yo‘q: {user.username}")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": message}

    response = requests.post(url, json=data)
    if response.status_code == 200:
        NotificationLog.objects.create(user=user, notification_type="telegram", status="sent")
        logger.info(f"Telegram message sent to {user.username}")
    else:
        logger.error(f"Telegram API error: {response.text}")


def save_user_chat_id(user_id, chat_id):
    """
    Foydalanuvchining Telegram chat ID sini bazaga saqlaydi.
    """
    try:
        user = User.objects.filter(id=user_id).first()
        if user:
            user.chat_id = chat_id
            user.save(update_fields=["chat_id"])
            logger.info(f"Foydalanuvchi {user.username} uchun chat ID ({chat_id}) saqlandi.")
        else:
            logger.warning(f"Foydalanuvchi topilmadi: ID {user_id}")
    except Exception as e:
        logger.error(f"Chat ID saqlashda xatolik: {e}")

