import threading
from threading import local
# Har bir so‘rov uchun foydalanuvchini saqlaydigan o‘zgaruvchi
_user_storage = threading.local()
_local = local()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class RequestMiddleware:
    """ Request obyektini global o‘zgaruvchi orqali saqlovchi middleware """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user_storage.user = request.user
        _local.ip = get_client_ip(request)
        response = self.get_response(request)
        return response

    @staticmethod
    def get_current_user():
        return getattr(_user_storage, "user", None)

    @staticmethod
    def get_current_ip():
        return getattr(_local, 'ip', None)

