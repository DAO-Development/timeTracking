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
    """Сериализация профилей пользователей"""

    class Meta:
        model = UserProfile
        fields = ('auth_user_id', 'name', 'lastname', 'photo_path', 'active', 'citizenship', 'birthdate',
                  'social_code_own', 'social_code_fin', 'address_own', 'address_fin', 'phone', 'phone_fin',
                  'bank_account', 'tax_number', 'auto', 'tool', 'english', 'estonian', 'finnish', 'russian',
                  'other_language', 'position', 'skills', 'boots', 'jacket', 'pants', 'shirt')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализация групп"""

    class Meta:
        model = Group
        fields = ('id', 'name')


class NewsSerializer(serializers.ModelSerializer):
    """Сериализация новостей"""

    class Meta:
        model = News
        fields = ('id', 'title', 'text', 'photo_path')


class NewsPostSerializer(serializers.ModelSerializer):
    """Сериализация новостей для POST"""

    class Meta:
        model = News
        fields = ('title', 'text', 'photo_path')


class ClientSerializer(serializers.ModelSerializer):
    """Сериализация клиентов"""

    class Meta:
        model = Client
        fields = '__all__'


class ClientPostSerializer(serializers.ModelSerializer):
    """Сериализация клиентов для POST"""

    class Meta:
        model = Client
        fields = '__all__'


class ClientEmployeesSerializer(serializers.ModelSerializer):
    """Сериализация сотрудников клиентов"""

    client = ClientSerializer()

    class Meta:
        model = ClientEmployees
        fields = '__all__'


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
                  'active', 'client_id', 'contact_id', 'habitation', 'accident_insurance', 'health_insurance')


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
