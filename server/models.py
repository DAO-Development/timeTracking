from django.db import models
from django.contrib.auth.models import User, Group


class UserProfile(models.Model):
    """Профиль пользователя"""
    auth_user_id = models.OneToOneField(User, models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(verbose_name='Имя', max_length=45)
    lastname = models.CharField(verbose_name='Фамилия', max_length=45)
    phone = models.CharField(verbose_name='Телефон', max_length=45)
    position = models.CharField(verbose_name='Должность', max_length=60)
    photo_path = models.CharField(verbose_name='Путь к фото', max_length=250)
    active = models.BooleanField(verbose_name='Работает')

    class Meta:
        db_table = "user_profile"
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


class Functions(models.Model):
    """Функции"""
    name = models.CharField(verbose_name="Название", max_length=45)

    class Meta:
        db_table = "functions"
        verbose_name = 'Функции'
        verbose_name_plural = 'Функции'


class GroupFunctions(models.Model):
    """Доступные группам функции"""
    group_id = models.ForeignKey(Group, models.CASCADE, verbose_name='Группа')
    functions_id = models.ForeignKey('Functions', models.CASCADE, verbose_name='Функция')

    class Meta:
        db_table = "group_functions"
        verbose_name = 'Доступные группам функции'
        verbose_name_plural = 'Доступные группам функции'


class UserContracts(models.Model):
    """Контракты рабочих"""
    create_date = models.DateField(verbose_name='Дата создания')
    path = models.CharField(verbose_name='Путь к файлу', max_length=250)
    photo_path = models.CharField(verbose_name='Путь к фото', max_length=250, null=True)
    user_profile_id = models.ForeignKey('UserProfile', models.CASCADE, verbose_name='Сотрудник')

    class Meta:
        db_table = "user_contracts"


class UserDocuments(models.Model):
    """Документы рабочих"""
    name = models.CharField(verbose_name='Название документа', max_length=100)
    create_date = models.DateField(verbose_name='Дата создания')
    path = models.CharField(verbose_name='Путь к файлу', max_length=250)
    photo_path = models.CharField(verbose_name='Путь к фото', max_length=250, null=True)
    user_profile_id = models.ForeignKey('UserProfile', models.CASCADE, verbose_name='Сотрудник')

    class Meta:
        db_table = "user_documents"


class News(models.Model):
    """Новости"""
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    text = models.TextField(verbose_name='Текст новости', max_length=1200)
    author = models.ForeignKey('UserProfile', models.CASCADE, verbose_name='Автор')

    class Meta:
        db_table = "news"


class Client(models.Model):
    name = models.CharField(verbose_name='Название юрлица', max_length=200)
    ogrn = models.CharField(verbose_name='ОГРН', max_length=13)
    business_address = models.CharField(verbose_name='Юр. адрес', max_length=250)
    warehouse_address = models.CharField(verbose_name='Адрес склада', max_length=250)
    phone = models.CharField(verbose_name='Телефон', max_length=45)
    email = models.CharField(verbose_name='Email', max_length=100)
    logo_path = models.CharField(verbose_name='Путь к логотипу', max_length=250)

    class Meta:
        db_table = "client"


class ClientEmployees(models.Model):
    """Штат фирмы клиента"""
    name = models.CharField(verbose_name='Имя', max_length=45)
    lastname = models.CharField(verbose_name='Фамилия', max_length=45)
    position = models.CharField(verbose_name='Должность', max_length=60)
    phone = models.CharField(verbose_name='Телефон', max_length=45)
    email = models.CharField(verbose_name='Email', max_length=100)

    class Meta:
        db_table = "client_employees"


class Objects(models.Model):
    """Объекты"""
    index = models.CharField(verbose_name='Индекс', max_length=6)
    city = models.CharField(verbose_name='Город', max_length=45)
    street = models.CharField(verbose_name='Улица', max_length=150)
    house = models.CharField(verbose_name='Дом', max_length=10)
    entrance = models.IntegerField(verbose_name='Подъезд', null=True)
    flat = models.CharField(verbose_name='Квартира', max_length=10)
    date_start = models.DateField(verbose_name='Дата начала')
    date_end = models.DateField(verbose_name='Дата завершения')
    active = models.BooleanField(verbose_name='Объект сдан')
    client_id = models.ForeignKey("Client", models.CASCADE, verbose_name='Клиент')

    class Meta:
        db_table = "objects"


class ObjectUser(models.Model):
    """Рабочие на объектах"""
    user_profile_id = models.ForeignKey("UserProfile", models.CASCADE, verbose_name='Пользователь')
    objects_id = models.ForeignKey("Objects", models.CASCADE, verbose_name='Объект')

    class Meta:
        db_table = "object_user"


class ObjectPhoto(models.Model):
    """Фото объектов"""
    photo_path = models.CharField(verbose_name='Путь к фото', max_length=250)
    objects_id = models.ForeignKey("Objects", models.CASCADE, verbose_name='Объект')

    class Meta:
        db_table = "object_photo"


class ObjectComments(models.Model):
    """Комментарии к объектам"""
    text = models.TextField(verbose_name="Текст комментария")
    user_profile_id = models.ForeignKey("UserProfile", models.CASCADE, verbose_name='Пользователь')
    objects_id = models.ForeignKey("Objects", models.CASCADE, verbose_name='Объект')
    object_comments_id = models.ForeignKey("ObjectComments", models.CASCADE, verbose_name='Родительский комментарий',
                                           null=True)

    class Meta:
        db_table = "object_comments"


class TimeReport(models.Model):
    """Часовые отчеты"""
    date = models.DateField(verbose_name='Дата')
    time_start = models.TimeField(verbose_name='Время начала')
    time_end = models.TimeField(verbose_name='Время конца')
    position = models.CharField(verbose_name='Должность', max_length=45)
    comment = models.TextField(verbose_name='Комментарий', max_length=1200)
    user_profile_id = models.ForeignKey("UserProfile", models.CASCADE, verbose_name='Пользователь')
    objects_id = models.ForeignKey("Objects", models.CASCADE, verbose_name='Объект')

    class Meta:
        db_table = "time_report"
