from django.shortcuts import render
from django.http import JsonResponse
from .utils import create_payme_payment


def initiate_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        order_id = request.POST.get('order_id')

        # Payme to'lovini yaratish
        response = create_payme_payment(amount, order_id)

        if response.get('status') == 'success':
            return JsonResponse(response)
        else:
            return JsonResponse({'error': 'To\'lov amalga oshmadi'})
