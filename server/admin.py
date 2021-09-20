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


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Functions, FunctionsAdmin)
admin.site.register(GroupFunctions, GroupFunctionsAdmin)
