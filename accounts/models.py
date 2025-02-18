from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    city = models.CharField(max_length=150)
    birth_date = models.DateField()

    # USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'city', 'birth_date']
