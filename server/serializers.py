from rest_framework import serializers

from server.models import *
from django.contrib.auth.models import User, Group


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователей"""

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_staff')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализация профилей пользователей"""

    auth_user_id = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('id', 'auth_user_id', 'name', 'lastname', 'phone', 'position', 'photo_path', 'active')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализация групп"""

    class Meta:
        model = Group
        fields = ('id', 'name')


class NewsSerializer(serializers.ModelSerializer):
    """Сериализация новостей"""

    class Meta:
        model = News
        fields = ('id', 'title', 'text', 'author')


class NewsPostSerializer(serializers.ModelSerializer):
    """Сериализация новостей для POST"""

    class Meta:
        model = News
        fields = ('title', 'text', 'author')


class ClientSerializer(serializers.ModelSerializer):
    """Сериализация клиентов"""

    class Meta:
        model = Client
        fields = ('id', 'name', 'ogrn', 'logo_path')


class ClientPostSerializer(serializers.ModelSerializer):
    """Сериализация клиентов для POST"""

    class Meta:
        model = Client
        fields = ('name', 'ogrn', 'logo_path')


class ObjectsSerializer(serializers.ModelSerializer):
    """Сериализация объектов"""

    client_id = ClientSerializer()

    class Meta:
        model = Objects
        fields = ('id', 'index', 'city', 'street', 'house', 'entrance', 'flat', 'date_start', 'date_end',
                  'active', 'client_id')


class ObjectsPostSerializer(serializers.ModelSerializer):
    """Сериализация объектов для POST"""

    class Meta:
        model = Objects
        fields = ('index', 'city', 'street', 'house', 'entrance', 'flat', 'date_start', 'date_end',
                  'active', 'client_id')


class ObjectUserSerializer(serializers.ModelSerializer):
    """Сериализация рабочих на объектах"""

    class Meta:
        model = ObjectUser
        fields = ('id', 'user_profile_id', 'objects_id')


class ObjectUserPostSerializer(serializers.ModelSerializer):
    """Сериализация рабочих на объектах"""

    class Meta:
        model = ObjectUser
        fields = ('user_profile_id', 'objects_id')
