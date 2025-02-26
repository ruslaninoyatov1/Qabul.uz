from django.contrib import admin

from .models import Application, Document
# Register your models here.


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['owner', 'branch', 'city','uploaded_date', 'status', 'time_to_come', 'location']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['owner', 'uploaded_at']
