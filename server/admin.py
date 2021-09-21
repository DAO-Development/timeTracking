from django.contrib import admin
from server.models import *


class UserProfileAdmin(admin.ModelAdmin):
    """Профили пользователей"""
    list_display = ('auth_user_id', 'name', 'lastname', 'position', 'active')


class FunctionsAdmin(admin.ModelAdmin):
    """Функции"""
    list_display = ('id', 'name')


class GroupFunctionsAdmin(admin.ModelAdmin):
    """Доступные группам функции"""
    list_display = ('group_id', 'functions_id')


class ClientsAdmin(admin.ModelAdmin):
    """Клиенты"""
    list_display = ('name', 'phone', 'email')


class ObjectsAdmin(admin.ModelAdmin):
    """Клиенты"""
    list_display = ('index', 'date_start', 'date_end', 'client_id')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Functions, FunctionsAdmin)
admin.site.register(GroupFunctions, GroupFunctionsAdmin)
admin.site.register(Client, ClientsAdmin)
admin.site.register(Objects, ObjectsAdmin)
