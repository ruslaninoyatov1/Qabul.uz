from celery import shared_task

@shared_task
def example_task(order_id):
    # To'lovni amalga oshirish uchun vazifa
    print(f'To\'lovni amalga oshirish vazifasi: {order_id}')
