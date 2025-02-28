from django.contrib import admin

from .models import CustomUser, Branch, City, CustomRole
# Register your models here.


@admin.register(CustomRole)
class CustomRoleAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'city', 'birth_date', 'role']


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'opened_date']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', ]

