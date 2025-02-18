import requests
from django.http import JsonResponse
from .models import Payment


def process_payment(request):
    provider = request.GET.get('provider')  # Click, Payme, Xumo, Uzcard, Visa
    amount = request.GET.get('amount')

    if provider not in ['Click', 'Payme', 'Xumo', 'Uzcard', 'Visa']:
        return JsonResponse({'error': 'Invalid provider'}, status=400)

    payment = Payment.objects.create(provider=provider, amount=amount, status='pending')

    # Bu yerda har bir payment provider uchun API chaqiramiz
    if provider == "Click":
        response = requests.post("https://click.uz/api/payment", data={"amount": amount})
    elif provider == "Payme":
        response = requests.post("https://payme.uz/api/payment", data={"amount": amount})
    # Xumo, Uzcard, Visa uchun ham xuddi shunday

    if response.status_code == 200:
        payment.status = "success"
    else:
        payment.status = "failed"

    payment.save()
    return JsonResponse({'status': payment.status})


# payments/views.py
from django.http import JsonResponse

def payme_payment(request):
    # API chaqiruvini yoki to'lovni tekshirish logikasini bu yerda qo'shing
    return JsonResponse({"status": "success"})


# views.py
from django.http import HttpResponse
from django_redis import get_redis_connection

def redis_test(request):
    # Redisga yozish
    r = get_redis_connection("default")
    r.set('my_key', 'Hello, Redis')

    # Redisdan o'qish
    value = r.get('my_key').decode('utf-8')

    return HttpResponse(f'Redisdan olingan qiymat: {value}')


# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Payment


def initiate_payment(request):
    # To'lov tizimiga qarab, talabni yuborish
    payment_method = request.POST.get('payment_method')
    amount = request.POST.get('amount')

    if payment_method == 'Click':
        # Click API orqali to'lovni amalga oshirish
        pass
    elif payment_method == 'Payme':
        # Payme API orqali to'lovni amalga oshirish
        pass
    elif payment_method == 'Visa':
        # Visa API orqali to'lovni amalga oshirish
        pass
    # Boshqa tizimlar uchun shunga o'xshash kod yozilishi kerak

    # Paymentni bazaga saqlash
    payment = Payment.objects.create(user=request.user, amount=amount, payment_method=payment_method, status='Pending',
                                     transaction_id='random-id')

    return JsonResponse({'status': 'success', 'payment_id': payment.id})


# views.py
from django.shortcuts import render
from .models import Payment

def check_payment_status(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
        if payment.status == 'Completed':
            return render(request, 'payment_status.html', {'status': 'To\'lov tasdiqlandi', 'payment': payment})
        else:
            return render(request, 'payment_status.html', {'status': 'To\'lov rad etildi', 'payment': payment})
    except Payment.DoesNotExist:
        return render(request, 'payment_status.html', {'status': 'To\'lov topilmadi'})



from django.http import JsonResponse
from .models import Payment

def create_payment(request):
    if request.method == "POST":
        provider = request.POST.get('provider')
        amount = request.POST.get('amount')
        status = request.POST.get('status', 'pending')
        transaction_id = request.POST.get('transaction_id', None)  # Optional transaction ID
        user = request.user if request.user.is_authenticated else None  # Associate user if logged in

        payment = Payment.objects.create(
            provider=provider,
            amount=amount,
            status=status,
            transaction_id=transaction_id,
            user=user
        )

        return JsonResponse({
            "message": "Payment created successfully!",
            "payment_id": payment.id,
            "provider": payment.provider,
            "amount": payment.amount,
            "status": payment.status,
            "transaction_id": payment.transaction_id,
            "user": payment.user.username if payment.user else None
        })
    return JsonResponse({"message": "Invalid method"}, status=405)
