from django.contrib import admin
from server.models import *


class UserProfileAdmin(admin.ModelAdmin):
    """Профили пользователей"""
    list_display = ('auth_user_id', 'name', 'lastname', 'position', 'active')


class UserDocumentsAdmin(admin.ModelAdmin):
    """Документы пользователей"""
    list_display = ('name', 'create_date', 'user_profile_id')


class FunctionsAdmin(admin.ModelAdmin):
    """Функции"""
    list_display = ('id', 'name')


class GroupFunctionsAdmin(admin.ModelAdmin):
    """Доступные группам функции"""
    list_display = ('group_id', 'functions_id')


class ClientsAdmin(admin.ModelAdmin):
    """Клиенты"""
    list_display = ('name', 'phone', 'email')


class ClientEmployeesAdmin(admin.ModelAdmin):
    """Штат клиентов"""
    list_display = ('lastname', 'name', 'email', 'phone', 'client')


class ObjectsAdmin(admin.ModelAdmin):
    """Объекты"""
    list_display = ('index', 'date_start', 'date_end', 'client_id')


class ObjectUserAdmin(admin.ModelAdmin):
    """Рабочие на объектах"""
    list_display = ('user_profile_id', 'objects_id')


class ObjectCommentsAdmin(admin.ModelAdmin):
    """Комментарии к объектам"""
    list_display = ('id', 'user_profile_id', 'objects_id')


class DocumentsModeAdmin(admin.ModelAdmin):
    """Типы документов"""
    list_display = ('id', 'name')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserDocuments, UserDocumentsAdmin)
admin.site.register(Functions, FunctionsAdmin)
admin.site.register(GroupFunctions, GroupFunctionsAdmin)
admin.site.register(Client, ClientsAdmin)
admin.site.register(ClientEmployees, ClientEmployeesAdmin)
admin.site.register(Objects, ObjectsAdmin)
admin.site.register(ObjectUser, ObjectUserAdmin)
admin.site.register(ObjectComments, ObjectCommentsAdmin)
admin.site.register(DocumentsMode, DocumentsModeAdmin)
