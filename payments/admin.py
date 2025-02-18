from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('provider', 'amount', 'status', 'created_at', 'updated_at', 'transaction_id', 'user')
    search_fields = ('provider', 'transaction_id', 'status')
    list_filter = ('status', 'provider')
