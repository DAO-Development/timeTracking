from rest_framework import serializers

from server.models import *
from django.contrib.auth.models import User, Group


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователей"""

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_staff', 'last_login')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            is_staff=validated_data['is_staff'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            instance.set_password(validated_data['password'])
        if "username" in validated_data:
            instance.username = validated_data["username"]
            instance.email = validated_data["email"]
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализация профилей пользователей"""

    auth_user_id = UserSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfilePostSerializer(serializers.ModelSerializer):
    """Сериализация профилей пользователей для POST-запросов"""

    class Meta:
        model = UserProfile
        fields = ('auth_user_id', 'name', 'lastname', 'photo_path', 'active', 'citizenship', 'birthdate',
                  'social_code_own', 'social_code_fin', 'address_own', 'address_fin', 'phone', 'phone_fin',
                  'bank_account', 'tax_number', 'auto', 'tool', 'english', 'estonian', 'finnish', 'russian',
                  'other_language', 'position', 'skills', 'boots', 'jacket', 'pants', 'shirt', 'create_date')


class UserDocumentsSerializer(serializers.ModelSerializer):
    """Сериализация документов пользователей"""

    class Meta:
        model = UserDocuments
        fields = '__all__'


class UserDocumentsPostSerializer(serializers.ModelSerializer):
    """Сериализация документов пользователей для POST-запросов"""

    class Meta:
        model = UserDocuments
        fields = ('name', 'create_date', 'path', 'user_profile_id')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализация групп"""

    class Meta:
        model = Group
        fields = ('id', 'name')


class GroupPostSerializer(serializers.ModelSerializer):
    """Сериализация групп для POST-запросов"""

    class Meta:
        model = Group
        fields = 'name'


class FunctionSerializer(serializers.ModelSerializer):
    """Сериализация функций для групп"""

    class Meta:
        model = Functions
        fields = '__all__'


class GroupFunctionsSerializer(serializers.ModelSerializer):
    """Сериализация функций групп"""

    class Meta:
        model = GroupFunctions
        fields = '__all__'


class GroupFunctionsPostSerializer(serializers.ModelSerializer):
    """Сериализация функций групп для POST-запросов"""

    class Meta:
        model = GroupFunctions
        fields = ('group_id', 'functions_id', 'edit', 'read')


class NewsSerializer(serializers.ModelSerializer):
    """Сериализация новостей"""

    class Meta:
        model = News
        fields = ('id', 'title', 'text', 'photo_path', 'create_date')


class NewsPostSerializer(serializers.ModelSerializer):
    """Сериализация новостей для POST"""

    class Meta:
        model = News
        fields = ('title', 'text', 'photo_path', 'create_date')


class ClientSerializer(serializers.ModelSerializer):
    """Сериализация клиентов"""

    class Meta:
        model = Client
        fields = '__all__'


class ClientPostSerializer(serializers.ModelSerializer):
    """Сериализация клиентов для POST"""

    class Meta:
        model = Client
        fields = (
            'name', 'short_name', 'ogrn', 'business_address', 'warehouse_address', 'phone', 'email', 'site',
            'logo_path', 'vat', 'branch', 'bank_account', 'bank', 'bic', 'account_operator', 'index_operator',
            'electronic_number', 'account_email', 'create_date')


class ClientEmployeesSerializer(serializers.ModelSerializer):
    """Сериализация сотрудников клиентов"""

    client = ClientSerializer()

    class Meta:
        model = ClientEmployees
        fields = '__all__'


class ClientEmployeesPostSerializer(serializers.ModelSerializer):
    """Сериализация сотрудников клиентов для POST-запросов"""

    class Meta:
        model = ClientEmployees
        fields = ('name', 'lastname', 'position', 'phone', 'work_phone', 'email', 'work_email', 'client', 'photo_path')


class ObjectsSerializer(serializers.ModelSerializer):
    """Сериализация объектов"""

    client_id = ClientSerializer()
    contact_id = ClientEmployeesSerializer()

    class Meta:
        model = Objects
        fields = '__all__'


class ObjectsPostSerializer(serializers.ModelSerializer):
    """Сериализация объектов для POST"""

    class Meta:
        model = Objects
        fields = ('index', 'city', 'street', 'house', 'entrance', 'flat', 'date_start', 'date_end',
                  'active', 'client_id', 'contact_id', 'habitation', 'accident_insurance', 'health_insurance',
                  'create_date')


class ObjectUserSerializer(serializers.ModelSerializer):
    """Сериализация рабочих на объектах"""

    user_profile_id = UserProfileSerializer()

    class Meta:
        model = ObjectUser
        fields = '__all__'


class ObjectUserPostSerializer(serializers.ModelSerializer):
    """Сериализация рабочих на объектах"""

    class Meta:
        model = ObjectUser
        fields = ('user_profile_id', 'objects_id', 'start_date', 'end_date', 'comment')


class ObjectPhotoSerializer(serializers.ModelSerializer):
    """Сериализация рабочих на объектах"""

    class Meta:
        model = ObjectPhoto
        fields = ('id', 'photo_path', 'objects_id')


class ObjectPhotoPostSerializer(serializers.ModelSerializer):
    """Сериализация рабочих на объектах"""

    class Meta:
        model = ObjectPhoto
        fields = ('photo_path', 'objects_id')


class ObjectCommentsSerializer(serializers.ModelSerializer):
    """Сериализация комментариев к объектам"""

    objects_id = ObjectsSerializer()
    user_profile_id = UserProfileSerializer()

    class Meta:
        model = ObjectComments
        fields = '__all__'


class ObjectCommentsPostSerializer(serializers.ModelSerializer):
    """Сериализация комментариев к объектам"""

    class Meta:
        model = ObjectComments
        fields = ('text', 'user_profile_id', 'objects_id', 'object_comments_id')


class NotesSerializer(serializers.ModelSerializer):
    """Сериализация виджета блокнота"""

    class Meta:
        model = Notes
        fields = '__all__'


class NotesPostSerializer(serializers.ModelSerializer):
    """Сериализация виджета блокнота для POST-запросов"""

    class Meta:
        model = Notes
        fields = ('color', 'text', 'user')
