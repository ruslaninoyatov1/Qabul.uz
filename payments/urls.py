from django.urls import path
from .views import process_payment

urlpatterns = [
    path('pay/', process_payment),
]
