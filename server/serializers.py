from django.core.mail import send_mail
from rest_framework import serializers

from server.models import *
from django.contrib.auth.models import User, Group

from timeTrack import settings


class GroupSerializer(serializers.ModelSerializer):
    """Сериализация групп"""

    class Meta:
        model = Group
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователей"""

    # groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'
        # fields = ('id', 'username', 'email', 'password', 'is_staff', 'last_login')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        # if settings.DJOSER['SEND_ACTIVATION_EMAIL']:
        # user.is_active = False
        # user.save(update_fields=["is_active"])
        context = {"user": user}
        # to = [user.email]
        # send_mail("Register work24",
        #           "You have been registered at work24. Your password: " + validated_data['password'],
        #           'polya.bagrowa@yandex.ru', [validated_data['email']])
        # if settings.DJOSER['SEND_ACTIVATION_EMAIL']:
        #     settings.DJOSER['EMAIL']['activation'](self.request, context).send(to)
        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            instance.set_password(validated_data['password'])
        if "username" in validated_data:
            instance.username = validated_data["username"]
            instance.email = validated_data["email"]
        instance.save()
        return instance


class PositionProfileSerializer(serializers.ModelSerializer):
    """Сериализация специальностей пользователей"""

    class Meta:
        model = PositionProfile
        fields = '__all__'


class CardsSerializer(serializers.ModelSerializer):
    """Сериализация карточек"""

    class Meta:
        model = Cards
        fields = '__all__'


class CardsUsersSerializer(serializers.ModelSerializer):
    """Сериализация карточек с пользователями"""

    card = CardsSerializer()

    class Meta:
        model = CardsUsers
        fields = '__all__'


class CardsUsersPostSerializer(serializers.ModelSerializer):
    """Сериализация карточек с пользователями для POST-запросов"""

    class Meta:
        model = CardsUsers
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализация профилей пользователей"""

    auth_user_id = UserSerializer()
    position = PositionProfileSerializer()
    cardsusers_set = CardsUsersSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfilePostSerializer(serializers.ModelSerializer):
    """Сериализация профилей пользователей для POST-запросов"""

    class Meta:
        model = UserProfile
        fields = ('auth_user_id', 'name', 'lastname', 'photo_path', 'active', 'citizenship', 'birthdate',
                  'social_code_own', 'social_code_fin', 'address_own', 'address_fin', 'phone', 'phone_fin',
                  'bank_account', 'tax_number', 'auto', 'auto_category', 'tool', 'english', 'estonian', 'finnish',
                  'russian', 'other_language', 'position', 'skills', 'boots', 'jacket', 'pants', 'shirt', 'create_date')


class UserDocumentsSerializer(serializers.ModelSerializer):
    """Сериализация документов пользователей"""

    class Meta:
        model = UserDocuments
        fields = '__all__'


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


class NewsSerializer(serializers.ModelSerializer):
    """Сериализация новостей"""

    class Meta:
        model = News
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    """Сериализация клиентов"""

    class Meta:
        model = Client
        fields = '__all__'


class ClientCommentsSerializer(serializers.ModelSerializer):
    """Сериализация комментариев к клиентам"""
    user_profile = UserProfileSerializer()

    class Meta:
        model = ClientComments
        fields = '__all__'


class ClientCommentsPostSerializer(serializers.ModelSerializer):
    """Сериализация комментариев к клиентам для POST-запросов"""

    class Meta:
        model = ClientComments
        fields = '__all__'


class PositionClientSerializer(serializers.ModelSerializer):
    """Сериализация должностей клиентов"""

    class Meta:
        model = PositionClient
        fields = '__all__'


class ClientEmployeesSerializer(serializers.ModelSerializer):
    """Сериализация сотрудников клиентов"""

    client = ClientSerializer()
    position = PositionClientSerializer()

    class Meta:
        model = ClientEmployees
        fields = '__all__'


class ClientEmployeesPostSerializer(serializers.ModelSerializer):
    """Сериализация сотрудников клиентов для POST-запросов"""

    class Meta:
        model = ClientEmployees
        fields = '__all__'


class ContactCommentsSerializer(serializers.ModelSerializer):
    """Сериализация комментариев к контактам"""
    user_profile = UserProfileSerializer()

    class Meta:
        model = ContactComments
        fields = '__all__'


class ContactCommentsPostSerializer(serializers.ModelSerializer):
    """Сериализация комментариев к контактам для POST-запросов"""

    class Meta:
        model = ContactComments
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
        fields = '__all__'


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
        fields = '__all__'


class ObjectPhotoSerializer(serializers.ModelSerializer):
    """Сериализация фото объектов"""

    class Meta:
        model = ObjectPhoto
        fields = '__all__'


class ObjectCommentsSerializer(serializers.ModelSerializer):
    """Сериализация комментариев к объектам"""

    objects_id = ObjectsSerializer()
    user_profile_id = UserProfileSerializer()

    class Meta:
        model = ObjectComments
        fields = '__all__'


class ObjectCommentsPostSerializer(serializers.ModelSerializer):
    """Сериализация комментариев к объектам для POST-запросов"""

    class Meta:
        model = ObjectComments
        fields = '__all__'


class NotesSerializer(serializers.ModelSerializer):
    """Сериализация виджета блокнота"""

    class Meta:
        model = Notes
        fields = '__all__'


class ChequeCategorySerializer(serializers.ModelSerializer):
    """Сериализация категорий чеков"""

    class Meta:
        model = ChequeCategory
        fields = '__all__'


class TermSerializer(serializers.ModelSerializer):
    """Сериализация сроков для счетов"""

    class Meta:
        model = Term
        fields = '__all__'


class ItemsSerializer(serializers.ModelSerializer):
    """Сериализация товаров/услуг"""

    class Meta:
        model = Items
        fields = '__all__'


class TaxSerializer(serializers.ModelSerializer):
    """Сериализация налога"""

    class Meta:
        model = Tax
        fields = '__all__'


class ChequeDocumentsSerializer(serializers.ModelSerializer):
    """Сериализация фото чеков"""

    class Meta:
        model = ChequeDocuments
        fields = '__all__'


class PurchasesSerializer(serializers.ModelSerializer):
    """Сериализация покупок"""

    user_profile = UserProfileSerializer()
    category = ChequeCategorySerializer()
    tax = TaxSerializer()

    class Meta:
        model = Purchases
        fields = '__all__'


class PurchasesPostSerializer(serializers.ModelSerializer):
    """Сериализация покупок для POST-запросов"""

    class Meta:
        model = Purchases
        fields = '__all__'


class SalesSerializer(serializers.ModelSerializer):
    """Сериализация продаж (счетов)"""

    object = ObjectsSerializer()
    payment_terms = TermSerializer()
    client = ClientSerializer()

    class Meta:
        model = Sales
        fields = '__all__'


class SalesPostSerializer(serializers.ModelSerializer):
    """Сериализация продаж (счетов) для POST-запросов"""

    class Meta:
        model = Sales
        fields = '__all__'


class DocumentsModeSerializer(serializers.ModelSerializer):
    """Сериализация типов документов"""

    class Meta:
        model = DocumentsMode
        fields = '__all__'


class DocumentsAccountingSerializer(serializers.ModelSerializer):
    """Сериализация документов бухгалтерии"""

    class Meta:
        model = DocumentsAccounting
        fields = '__all__'


class DocumentsClientSerializer(serializers.ModelSerializer):
    """Сериализация документов с клиентами"""

    client = ClientSerializer()

    class Meta:
        model = DocumentsClient
        fields = '__all__'


class DocumentsClientPostSerializer(serializers.ModelSerializer):
    """Сериализация документов с клиентами для POST-запросов"""

    class Meta:
        model = DocumentsClient
        fields = '__all__'


class WaybillGoalSerializer(serializers.ModelSerializer):
    """Сериализация целей поездок"""

    class Meta:
        model = WaybillGoal
        fields = '__all__'


class WaybillSerializer(serializers.ModelSerializer):
    """Сериализация путевых листов"""

    user_profile = UserProfileSerializer()
    goal = WaybillGoalSerializer()

    class Meta:
        model = Waybill
        fields = '__all__'


class WaybillPostSerializer(serializers.ModelSerializer):
    """Сериализация путевых листов для POST-запросов"""

    class Meta:
        model = Waybill
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    """Сериализация Предложений"""

    author = UserProfileSerializer()
    term = TermSerializer()
    client = ClientSerializer()
    contact = UserProfileSerializer()
    object = ObjectsSerializer()

    class Meta:
        model = Offer
        fields = '__all__'


class OfferPostSerializer(serializers.ModelSerializer):
    """Сериализация Предложений для POST-запросов"""

    class Meta:
        model = Offer
        fields = ['id', 'create_date', 'author', 'active', 'client', 'contact', 'object', 'term', 'from_client']


class CalendarSerializer(serializers.ModelSerializer):
    """Сериализация событий календаря"""

    class Meta:
        model = Calendar
        fields = '__all__'


class TimeReportSerializer(serializers.ModelSerializer):
    """Сериализация часовых отчетов"""
    user_profile_id = UserProfileSerializer()
    objects_id = ObjectsSerializer()

    class Meta:
        model = TimeReport
        fields = '__all__'


class TimeReportPostSerializer(serializers.ModelSerializer):
    """Сериализация часовых отчетов для POST-запросов"""

    class Meta:
        model = TimeReport
        fields = '__all__'


class UserSettingsSerializer(serializers.ModelSerializer):
    """Сериализация настроек пользователя"""

    class Meta:
        model = UserSettings
        fields = '__all__'
