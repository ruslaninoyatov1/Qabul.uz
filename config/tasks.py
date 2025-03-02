from celery import shared_task
from logs.models import LogEntry
from django.contrib.auth import get_user_model
import logging
user = get_user_model()


@shared_task
def add(x, y):
    return x + y


@shared_task
def log_action_task(user_id, action, app_name, model_name, object_id, ip_address):

    LogEntry.objects.create(
        user_id=user_id,
        app_name=app_name,
        model_name=model_name,
        object_id=object_id,
        action=action,
        ip_address=ip_address,


    )



from celery import shared_task
from django.contrib.auth import get_user_model
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


@shared_task
def save_chat_id_task(user_id, chat_id):
    """
    Celery vazifasi: Foydalanuvchining chat ID sini asinxron saqlaydi.
    """
    user = User.objects.filter(id=user_id).first()
    if user:
        user.chat_id = chat_id
        user.save(update_fields=["chat_id"])
        logger.info(f"Chat ID {chat_id} foydalanuvchi {user.username} uchun saqlandi.")
        return "Chat ID saqlandi"
    return "Foydalanuvchi topilmadi"
