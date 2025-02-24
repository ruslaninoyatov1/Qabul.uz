from django.db import models
from django.core.exceptions import ValidationError

from accounts.models import CustomUser, Branch, City
from .validators import validate_file_extension
# Create your models here.


"""Hujjat"""
class Document(models.Model):
    file = models.FileField(verbose_name='Hujjat', upload_to='documents/', validators=[validate_file_extension])
    owner = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name='Foydalanuvchi')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuklangan vaqt")

    def __str__(self):
         return self.owner.username


"""Ariza"""
class Application(models.Model):

    DOCUMENT_STATUS = [
        ("Ko'rib chiqilmoqda", "Ko'rib chiqilmoqda"),
        ("Qabul qilindi", "Qabul qilindi"),
        ("Rad etildi", "Rad etildi")
    ]

    documents = models.ManyToManyField(Document, verbose_name='Hujjatlar')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, verbose_name="Filial")
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='Shahar')
    uploaded_date = models.DateTimeField(auto_now_add=True, verbose_name="Yuklangan sana")
    status = models.CharField(max_length=100, choices=DOCUMENT_STATUS, verbose_name="Holat")
    reason = models.TextField(verbose_name="Rad etish sababi", null=True, blank=True)
    time_to_come = models.DateTimeField(null=True, blank=True, verbose_name="Vaqtni belgilash")

    def clean(self):
            if self.status == "Rad etildi" and not self.reason:
                raise ValidationError({"reason": "Rad etish sababi kiritilishi shart."})


    def __str__(self):
        return self.owner.username
