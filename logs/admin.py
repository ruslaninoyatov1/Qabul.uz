from django.contrib import admin
from .models import LogEntry, NotificationLog


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'app_name', 'model_name', 'action', 'object_id', 'ip_address')
    list_filter = ('app_name', 'model_name', 'action')
    search_fields = ('user__username', 'model_name', 'action')


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ("user", "notification_type", "status", "timestamp")
    search_fields = ("user__username", "notification_type", "status")
    list_filter = ("status", "notification_type")

