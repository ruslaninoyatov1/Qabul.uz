from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from accounts.models import CustomUser
from .models import LogEntry
from django.conf import settings
from .middleware import RequestMiddleware
from django.contrib.auth.models import AnonymousUser

APPS_TO_LOG = ["accounts", "applications", "payments"]


def create_log(instance, action):
    if instance._meta.app_label not in APPS_TO_LOG:
        return

    user = RequestMiddleware.get_current_user()
    ip_address = RequestMiddleware.get_current_ip()
    if isinstance(user, AnonymousUser):
        user = None

    LogEntry.objects.create(
        user=user,
        app_name=instance._meta.app_label,
        model_name=instance._meta.model_name,
        object_id=instance.pk,
        action=action,
        ip_address=ip_address
    )


@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    if sender == LogEntry:
        return

    action = "Created" if created else "Updated"
    create_log(instance, action)


@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender == LogEntry:
        return
    create_log(instance, "Deleted")
