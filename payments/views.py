from django.http import JsonResponse

def process_payment(request):
    return JsonResponse({"status": "success", "message": "Payment processing started"})
