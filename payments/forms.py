from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['provider', 'amount', 'status', 'transaction_id', 'user']
