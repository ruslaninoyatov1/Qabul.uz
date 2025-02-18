from django.urls import path
from . import views

urlpatterns = [
    path('check_payment/<int:payment_id>/', views.check_payment_status, name='check_payment_status'),
    path('redis_test/', views.redis_test, name='redis_test'),
    path('create-payment/', views.create_payment, name='create_payment'),
]
