from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class LogEntry(models.Model):
    APP_CHOICES = [
        ("accounts", "Accounts"),
        ("applications", "Applications"),
        ("payments", "Payments")
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Foydalanuvchi", related_name="custom_log_entries")
    app_name = models.CharField(max_length=50, choices=APP_CHOICES, verbose_name="Ilova nomi")
    model_name = models.CharField(max_length=100, verbose_name="Model nomi")
    object_id = models.IntegerField(verbose_name="Obyekt ID si")
    action = models.CharField(max_length=20, verbose_name="Harakat")  # "Created", "Updated", "Deleted"
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Vaqt")
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.app_name} - {self.model_name} - {self.action}"


class NotificationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="notifications")
    notification_type = models.CharField(max_length=50, choices=[("email", "Email"), ("telegram", "Telegram")])
    status = models.CharField(max_length=20, choices=[("sent", "Sent"), ("failed", "Failed")])
    error_message = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.notification_type} - {self.status}"
