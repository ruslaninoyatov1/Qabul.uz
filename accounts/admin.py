from django.contrib import admin

from .models import CustomUser, Branch, City, CustomRole
# Register your models here.


@admin.register(CustomRole)
class CustomRoleAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'city', 'birth_date', 'role', "telegram_name"]


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'opened_date']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', ]


# from django.contrib import admin
# from django_db_logger.models import StatusLog
# admin.site.unregister(StatusLog)
#
#
# @admin.register(StatusLog)
# class StatusLogAdmin(admin.ModelAdmin):
#     list_display = ('create_datetime', 'level', 'msg', 'trace')
#     list_filter = ('level', 'create_datetime', "logger_name")
#     search_fields = ('msg',)



