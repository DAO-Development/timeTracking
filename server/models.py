from django.db import models
from django.contrib.auth.models import User, Group


class PositionProfile(models.Model):
    name = models.CharField(verbose_name='Специальность', max_length=60)

    class Meta:
        db_table = "position_profile"
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности для профилей'


class UserProfile(models.Model):
    """Профиль пользователя"""
    auth_user_id = models.OneToOneField(User, models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(verbose_name='Имя', max_length=45)
    lastname = models.CharField(verbose_name='Фамилия', max_length=45)
    citizenship = models.CharField(verbose_name='Гражданство', max_length=45)
    birthdate = models.DateField(verbose_name='Дата рождения')
    social_code_own = models.CharField(verbose_name='Номер социального страхования', max_length=20, null=True,
                                       blank=True)
    social_code_fin = models.CharField(verbose_name='Финский номер социального страхования', max_length=20, null=True,
                                       blank=True)
    address_own = models.JSONField(verbose_name='Адрес в своей стране', null=True, blank=True)
    address_fin = models.JSONField(verbose_name='Адрес в Финляндии', null=True, blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=45, null=True, blank=True)
    phone_fin = models.CharField(verbose_name='Телефон в Финляндии', max_length=45, null=True, blank=True)
    # position = models.CharField(verbose_name='Специальность', max_length=60)
    position = models.ForeignKey('PositionProfile', models.RESTRICT, verbose_name='Специальность', null=True,
                                 blank=True)
    photo_path = models.CharField(verbose_name='Путь к фото', max_length=250, null=True, blank=True)
    active = models.BooleanField(verbose_name='Работает')
    bank_account = models.CharField(verbose_name='Счет в банке', max_length=31, null=True, blank=True)
    tax_number = models.CharField(verbose_name='Налоговый номер', max_length=30, null=True, blank=True)
    auto = models.BooleanField(verbose_name='Свой автомобиль', default=False)
    tool = models.BooleanField(verbose_name='Свой инструмент', default=False)
    english = models.BooleanField(verbose_name='Английский язык', default=False)
    estonian = models.BooleanField(verbose_name='Эстонский язык', default=False)
    finnish = models.BooleanField(verbose_name='Финский язык', default=False)
    russian = models.BooleanField(verbose_name='Русский язык', default=False)
    other_language = models.CharField(verbose_name='Другой язык', max_length=100, null=True, blank=True)
    skills = models.TextField(verbose_name='Что умеет делать', max_length=500, null=True, blank=True)

    boots = models.IntegerField(verbose_name='Ботинки', null=True, blank=True)
    jacket = models.IntegerField(verbose_name='Куртка', null=True, blank=True)
    pants = models.IntegerField(verbose_name='Штаны', null=True, blank=True)
    shirt = models.IntegerField(verbose_name='Футболка', null=True, blank=True)

    create_date = models.DateField(verbose_name="Дата создания", null=True)

    class Meta:
        db_table = "user_profile"
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


class Functions(models.Model):
    """Функции"""
    name = models.CharField(verbose_name="Компонент", max_length=45)
    text = models.CharField(verbose_name="Название", max_length=45)

    class Meta:
        db_table = "functions"
        verbose_name = 'Функции'
        verbose_name_plural = 'Функции'


class GroupFunctions(models.Model):
    """Доступные группам функции"""
    group_id = models.ForeignKey(Group, models.CASCADE, verbose_name='Группа')
    functions_id = models.ForeignKey('Functions', models.CASCADE, verbose_name='Функция')
    read = models.BooleanField(verbose_name="Чтение", null=True, blank=True, default=False)
    edit = models.BooleanField(verbose_name="Редактирование", null=True, blank=True, default=False)

    class Meta:
        db_table = "group_functions"
        verbose_name = 'Доступные группам функции'
        verbose_name_plural = 'Доступные группам функции'


class UserContracts(models.Model):
    """Контракты рабочих"""
    create_date = models.DateField(verbose_name='Дата создания')
    path = models.CharField(verbose_name='Путь к файлу', max_length=250)
    photo_path = models.CharField(verbose_name='Путь к фото', max_length=250, null=True, blank=True)
    user_profile_id = models.ForeignKey('UserProfile', models.RESTRICT, verbose_name='Сотрудник')

    class Meta:
        db_table = "user_contracts"


class UserDocuments(models.Model):
    """Документы рабочих"""
    name = models.CharField(verbose_name='Название документа', max_length=100)
    create_date = models.DateField(verbose_name='Дата создания')
    path = models.CharField(verbose_name='Путь к файлу', max_length=250)
    photo_path = models.CharField(verbose_name='Путь к фото', max_length=250, null=True, blank=True)
    user_profile_id = models.ForeignKey('UserProfile', models.RESTRICT, verbose_name='Сотрудник')

    class Meta:
        db_table = "user_documents"


class News(models.Model):
    """Новости"""
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    text = models.TextField(verbose_name='Текст новости', max_length=1200)
    photo_path = models.CharField(verbose_name='Обложка', max_length=250, null=True, blank=True)

    create_date = models.DateField(verbose_name="Дата создания", null=True)

    class Meta:
        db_table = "news"


class Client(models.Model):
    name = models.CharField(verbose_name='Название юрлица', max_length=200)
    short_name = models.CharField(verbose_name='Краткое название', max_length=50, null=True, blank=True)
    ogrn = models.CharField(verbose_name='ОГРН', max_length=13)
    business_address = models.JSONField(verbose_name='Юр. адрес')
    warehouse_address = models.JSONField(verbose_name='Адрес доставки', null=True, blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=45)
    email = models.CharField(verbose_name='Email', max_length=100)
    site = models.CharField(verbose_name='Сайт', max_length=300, null=True, blank=True)
    logo_path = models.CharField(verbose_name='Путь к логотипу', max_length=250, null=True, blank=True)
    vat = models.IntegerField(verbose_name='НДС', null=True, blank=True)
    branch = models.CharField(verbose_name='Отрасль', max_length=150, null=True, blank=True)
    bank_account = models.CharField(verbose_name='Номер счета в банке', max_length=31, null=True, blank=True)
    bank = models.CharField(verbose_name='Банк', max_length=200, null=True, blank=True)
    bic = models.CharField(verbose_name='BIC/SWIFT', max_length=11, null=True, blank=True)
    account_operator = models.CharField(verbose_name='Оператор электронных счетов', max_length=200, null=True,
                                        blank=True)
    index_operator = models.CharField(verbose_name='Индекс посредника', max_length=12, null=True, blank=True)
    electronic_number = models.CharField(verbose_name='Номер электронных счетов', max_length=31, null=True, blank=True)
    account_email = models.CharField(verbose_name='Email для счетов', max_length=100, null=True, blank=True)
    active = models.BooleanField(verbose_name='Активен', default=True)

    create_date = models.DateField(verbose_name="Дата создания", null=True)

    class Meta:
        db_table = "client"
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class ClientComments(models.Model):
    """Комментарии к клиентам"""
    text = models.TextField(verbose_name="Текст комментария")
    user_profile = models.ForeignKey("UserProfile", models.RESTRICT, verbose_name='Пользователь')
    client = models.ForeignKey("Client", models.CASCADE, verbose_name='Клиент')
    client_comments = models.ForeignKey("ClientComments", models.RESTRICT, verbose_name='Родительский комментарий',
                                        null=True, blank=True)

    class Meta:
        db_table = "client_comments"
        verbose_name = 'Комментарий к клиенту'
        verbose_name_plural = 'Комментарии к клиентам'


class PositionClient(models.Model):
    name = models.CharField(verbose_name='Специальность', max_length=60)

    class Meta:
        db_table = "position_client"
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности для клиентов'


class ClientEmployees(models.Model):
    """Штат фирмы клиента"""
    name = models.CharField(verbose_name='Имя', max_length=45)
    lastname = models.CharField(verbose_name='Фамилия', max_length=45)
    # position = models.CharField(verbose_name='Должность', max_length=60)
    position = models.ForeignKey('PositionClient', models.RESTRICT, verbose_name='Должность', null=True, blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=45)
    work_phone = models.CharField(verbose_name='Рабочий телефон', max_length=45, null=True, blank=True)
    email = models.CharField(verbose_name='Email', max_length=100)
    work_email = models.CharField(verbose_name='Рабочий Email', max_length=100, null=True, blank=True)
    client = models.ForeignKey(Client, models.RESTRICT, verbose_name='Фирма', null=True, blank=True)
    photo_path = models.CharField(verbose_name='Путь к фото', max_length=250, null=True, blank=True)
    active = models.BooleanField(verbose_name='Активен', default=True)

    class Meta:
        db_table = "client_employees"
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class ContactComments(models.Model):
    """Комментарии к контактам"""
    text = models.TextField(verbose_name="Текст комментария")
    user_profile = models.ForeignKey("UserProfile", models.RESTRICT, verbose_name='Пользователь')
    contact = models.ForeignKey("ClientEmployees", models.CASCADE, verbose_name='Клиент')
    contact_comments = models.ForeignKey("ContactComments", models.RESTRICT, verbose_name='Родительский комментарий',
                                         null=True, blank=True)

    class Meta:
        db_table = "contact_comments"
        verbose_name = 'Комментарий к контакту'
        verbose_name_plural = 'Комментарии к контактам'


class Objects(models.Model):
    """Объекты"""
    index = models.CharField(verbose_name='Индекс', max_length=12)
    city = models.CharField(verbose_name='Город', max_length=45)
    street = models.CharField(verbose_name='Улица', max_length=150)
    house = models.CharField(verbose_name='Дом', max_length=10)
    entrance = models.IntegerField(verbose_name='Подъезд', null=True, blank=True)
    flat = models.CharField(verbose_name='Квартира', max_length=10, null=True, blank=True)
    date_start = models.DateField(verbose_name='Начало работ')
    date_end = models.DateField(verbose_name='Конец работ')
    active = models.BooleanField(verbose_name='Объект сдан', default=False)
    client_id = models.ForeignKey("Client", models.RESTRICT, verbose_name='Клиент')
    contact_id = models.ForeignKey("ClientEmployees", models.RESTRICT, verbose_name='Контактное лицо')
    work_description = models.TextField(verbose_name='Описание работ', max_length=1500, null=True, blank=True)
    habitation = models.CharField(verbose_name='Жилье', max_length=100, null=True, blank=True)
    accident_insurance = models.CharField(verbose_name='Страховка от несчастных случаев', max_length=100, null=True,
                                          blank=True)
    health_insurance = models.CharField(verbose_name='Страховка здоровья', max_length=100, null=True, blank=True)
    photo_path = models.CharField(verbose_name='Фото', max_length=250, default="/objects/preview.jpg")
    create_date = models.DateField(verbose_name="Дата создания", null=True)

    class Meta:
        db_table = "objects"
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"


class ObjectUser(models.Model):
    """Рабочие на объектах"""
    user_profile_id = models.ForeignKey("UserProfile", models.RESTRICT, verbose_name='Пользователь')
    objects_id = models.ForeignKey("Objects", models.RESTRICT, verbose_name='Объект')
    start_date = models.DateField(verbose_name='Начало работ')
    end_date = models.DateField(verbose_name='Конец работ', null=True, blank=True)
    comment = models.TextField(verbose_name='Комментарий', max_length=1500, null=True, blank=True)

    class Meta:
        db_table = "object_user"
        verbose_name = "Рабочие на объектах"
        verbose_name_plural = "Рабочие на объектах"


class ObjectPhoto(models.Model):
    """Фото объектов"""
    photo_path = models.CharField(verbose_name='Путь к фото', max_length=250)
    objects_id = models.ForeignKey("Objects", models.CASCADE, verbose_name='Объект')

    class Meta:
        db_table = "object_photo"


class ObjectComments(models.Model):
    """Комментарии к объектам"""
    text = models.TextField(verbose_name="Текст комментария")
    user_profile_id = models.ForeignKey("UserProfile", models.RESTRICT, verbose_name='Пользователь')
    objects_id = models.ForeignKey("Objects", models.CASCADE, verbose_name='Объект')
    object_comments_id = models.ForeignKey("ObjectComments", models.RESTRICT, verbose_name='Родительский комментарий',
                                           null=True, blank=True)

    class Meta:
        db_table = "object_comments"
        verbose_name = 'Комментарий к объекту'
        verbose_name_plural = 'Комментарии к объектам'


class TimeReport(models.Model):
    """Часовые отчеты"""
    date = models.DateField(verbose_name='Дата')
    time_start = models.TimeField(verbose_name='Время начала')
    time_end = models.TimeField(verbose_name='Время конца')
    position = models.CharField(verbose_name='Должность', max_length=45)
    comment = models.TextField(verbose_name='Комментарий', max_length=1200)
    user_profile_id = models.ForeignKey("UserProfile", models.RESTRICT, verbose_name='Пользователь')
    objects_id = models.ForeignKey("Objects", models.RESTRICT, verbose_name='Объект')

    class Meta:
        db_table = "time_report"
        verbose_name = "Часовой отчет"
        verbose_name_plural = "Часовые отчеты"


class Notes(models.Model):
    """Виджеты"""
    last_save = models.DateTimeField(verbose_name="Последнее сохранение", auto_now=True)
    color = models.CharField(verbose_name="Цвет блокнота", max_length=7)
    text = models.TextField(verbose_name="Содержимое", max_length=1000)
    user = models.ForeignKey(User, models.CASCADE, verbose_name='Пользователь')

    class Meta:
        db_table = "notes"
        verbose_name = "Блокнот"
        verbose_name_plural = "Блокноты"


class ChequeCategory(models.Model):
    """Категории для чеков"""
    name = models.CharField(verbose_name="Название", max_length=100)

    class Meta:
        db_table = "cheque_category"
        verbose_name = "Категория чеков"
        verbose_name_plural = "Категории чеков"


class Term(models.Model):
    """Сроки"""
    days = models.IntegerField(verbose_name="Срок в днях")

    class Meta:
        db_table = "term"
        verbose_name = "Срок"
        verbose_name_plural = "Сроки"


class Tax(models.Model):
    """НДС"""
    tax = models.IntegerField(verbose_name="Налог в %")

    class Meta:
        db_table = "tax"
        verbose_name = "НДС"
        verbose_name_plural = "НДС"


class Purchases(models.Model):
    """Покупки"""
    user_profile = models.ForeignKey("UserProfile", on_delete=models.RESTRICT, verbose_name="Ответственный")
    category = models.ForeignKey("ChequeCategory", on_delete=models.RESTRICT, verbose_name="Категория")
    tax = models.ForeignKey("Tax", on_delete=models.RESTRICT, verbose_name="НДС", null=True, blank=True)
    payment_method = models.CharField(verbose_name="Способ оплаты", max_length=100)
    number = models.CharField(verbose_name="Номер счета", max_length=100, null=True, blank=True)
    date_receipt = models.DateField(verbose_name="Дата получения", null=True, blank=True)
    date = models.DateField(verbose_name="Дата покупки")
    place = models.CharField(verbose_name="Место покупки", max_length=150, null=True, blank=True)
    price = models.FloatField(verbose_name="Сумма покупки")
    bundle = models.CharField(verbose_name="от 2х чеков", max_length=100, null=True, blank=True)
    comment = models.TextField(verbose_name="Заметки", max_length=1000, null=True, blank=True)

    class Meta:
        db_table = "purchases"
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"


class Sales(models.Model):
    """Счета"""
    # todo Добавить поле "номер счета" - значение id+9999 - ИЗМЕНИТЬ МИГРАЦИЮ
    create_date = models.DateField(verbose_name="Дата покупки")
    object_number = models.CharField(verbose_name='Номер объекта', max_length=60, null=True, blank=True)
    client = models.ForeignKey("Client", models.RESTRICT, verbose_name="Клиент", null=True, blank=True)
    object = models.ForeignKey("Objects", models.RESTRICT, verbose_name="Объект", null=True, blank=True)
    comment = models.TextField(verbose_name="Заметки", max_length=1000, null=True, blank=True)
    description = models.TextField(verbose_name="Пояснение к счету", max_length=1000, null=True, blank=True)
    payment_terms = models.ForeignKey("Term", on_delete=models.RESTRICT, verbose_name="Срок оплаты")
    number_link = models.CharField(verbose_name="Номер ссылки", max_length=100, null=True, blank=True)
    status = models.CharField(verbose_name="Статус", max_length=30, default="Выставлен")
    items = models.ManyToManyField("Items", verbose_name="Товары/услуги", blank=True)
    remainder = models.IntegerField(verbose_name="Напоминание", null=True, blank=True)
    percent_delay = models.IntegerField(verbose_name="Процент по просрочке", null=True, blank=True)
    printed = models.BooleanField(verbose_name="Повторный счет", default=False)

    class Meta:
        db_table = "sales"
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"


class ChequeDocuments(models.Model):
    """Фото/pdf чеков"""
    path = models.CharField(verbose_name="Путь к файлу", max_length=250)
    purchases = models.ForeignKey("Purchases", on_delete=models.CASCADE, related_name="photos", verbose_name="Покупка",
                                  null=True, blank=True)
    sales = models.ForeignKey("Sales", on_delete=models.CASCADE, related_name="photos", verbose_name="Покупка",
                              null=True, blank=True)

    class Meta:
        db_table = "cheque_documents"
        verbose_name = "Фото чеков"
        verbose_name_plural = "Фото чеков"


class DocumentsMode(models.Model):
    name = models.CharField(verbose_name="Название", max_length=50)

    class Meta:
        db_table = "documents_mode"
        verbose_name = "Тип документа"
        verbose_name_plural = "Типы документов"


class DocumentsAccounting(models.Model):
    """Документы бухгалтерии: отчеты, выписки, документы на собственность"""
    name = models.CharField(verbose_name="Название", max_length=100)
    create_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    path = models.CharField(verbose_name="Путь к файлу", max_length=250)
    mode = models.ForeignKey("DocumentsMode", on_delete=models.RESTRICT, verbose_name="Тип документа")

    class Meta:
        db_table = "documents_accounting"
        verbose_name = "Бухгалтерский документ"
        verbose_name_plural = "Бухгалтерские документы"


class DocumentsClient(models.Model):
    """Документы с клиентами: договора, документы"""
    name = models.CharField(verbose_name="Название", max_length=100)
    create_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    path = models.CharField(verbose_name="Путь к файлу", max_length=250)
    client = models.ForeignKey("Client", on_delete=models.RESTRICT, verbose_name="Клиент")
    mode = models.ForeignKey("DocumentsMode", on_delete=models.RESTRICT, verbose_name="Тип документа")

    class Meta:
        db_table = "documents_client"
        verbose_name = "Документ с клиентом"
        verbose_name_plural = "Документы с клиентами"


class WaybillGoal(models.Model):
    """Цели поездок"""
    name = models.CharField(verbose_name="Название", max_length=100)

    class Meta:
        db_table = "waybill_goal"
        verbose_name = "Цель поездки"
        verbose_name_plural = "Цели поездок"


class Waybill(models.Model):
    """Путевые листы"""
    date_start = models.DateField(verbose_name="Дата начала поездки", null=True)
    date_end = models.DateField(verbose_name="Дата конца поездки", null=True)
    departure = models.CharField(verbose_name="Пункт отправления", max_length=250)
    destination = models.CharField(verbose_name="Пункт назначенния", max_length=250)
    kilometrage_start = models.IntegerField(verbose_name="Километраж в начале поездки", null=True)
    kilometrage_end = models.IntegerField(verbose_name="Километраж в конце поездки", null=True)
    user_profile = models.ForeignKey("UserProfile", on_delete=models.RESTRICT, verbose_name="Профиль")
    time_start = models.TimeField(verbose_name="Время начала поездки")
    time_end = models.TimeField(verbose_name="Время конца поездки")
    goal = models.ForeignKey("WaybillGoal", on_delete=models.RESTRICT, verbose_name="Цель поездки")
    auto_mark = models.CharField(verbose_name="Марка автомобиля", max_length=100)
    auto_type = models.CharField(verbose_name="Тип коробки", max_length=60)
    auto_fuel = models.CharField(verbose_name="Тип топлива", max_length=60)

    class Meta:
        db_table = "waybill"
        verbose_name = "Путевой лист"
        verbose_name_plural = "Путевые листы"


class Items(models.Model):
    """Товары и услуги"""
    name = models.CharField(verbose_name="Название", max_length=100)
    price = models.FloatField(verbose_name="Стоимость без налога")
    tax = models.IntegerField(verbose_name="НДС", null=True, blank=True)
    discount = models.IntegerField(verbose_name="Скидка (%)", null=True, blank=True)
    quantity = models.FloatField(verbose_name="Количество", null=True, blank=True)
    measurement = models.CharField(verbose_name="Единицы измерения", max_length=20, null=True, blank=True)
    type = models.CharField(verbose_name="Тип", max_length=50, default="material")

    class Meta:
        db_table = "items"
        verbose_name = "Товар/услуга"
        verbose_name_plural = "Товары/услуги"


class Offer(models.Model):
    """Предложения"""
    create_date = models.DateField(verbose_name="Дата создания", auto_now_add=True, null=True, blank=True)
    author = models.ForeignKey("UserProfile", on_delete=models.RESTRICT, verbose_name="Автор", null=True)
    active = models.BooleanField(verbose_name="Активно", default=True)
    term = models.ForeignKey("Term", on_delete=models.RESTRICT, verbose_name="Срок предложения")
    client = models.ForeignKey("Client", on_delete=models.RESTRICT, verbose_name="Клиент")
    items = models.ManyToManyField("Items", verbose_name="Товары/услуги")
    from_client = models.JSONField(verbose_name="От заказчика", null=True, blank=True)

    class Meta:
        db_table = "offer"
        verbose_name = "Предложение"
        verbose_name_plural = "Предложения"


class Calendar(models.Model):
    """Календарь"""
    # todo сделать author not Null
    author = models.ForeignKey("UserProfile", verbose_name="Автор", related_name='author', on_delete=models.CASCADE,
                               null=True)
    profile = models.ForeignKey("UserProfile", verbose_name="Пользователь", on_delete=models.CASCADE, null=True,
                                blank=True)
    group = models.ForeignKey(Group, verbose_name="Группа", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name="Название", max_length=100)
    start = models.DateTimeField(verbose_name="Дата и время начала")
    end = models.DateTimeField(verbose_name="Дата и время конца", null=True, blank=True, default=None)
    allDay = models.BooleanField(verbose_name="Весь день", default=False)
    color = models.CharField(verbose_name="Цвет", max_length=30, null=True, blank=True)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)

    class Meta:
        db_table = "calendar"
        verbose_name = "Календарь"
        verbose_name_plural = "Календарь"


class UserSettings(models.Model):
    user_profile = models.OneToOneField("UserProfile", on_delete=models.CASCADE, verbose_name="Профиль")
    theme = models.CharField(verbose_name="Тема", max_length=10, default="light")
    language = models.CharField(verbose_name="Язык", max_length=2, default="ru")

    class Meta:
        db_table = "user_settings"
        verbose_name = "Настройки польщователя"
        verbose_name_plural = "Настройки пользователя"
# class WidgetUser(models.Model):
#     """Виджеты"""
#     name = models.CharField(verbose_name="Название виджета", max_length=120)
#     user = models.ForeignKey("User", models.CASCADE, verbose_name='Пользователь')
#
#     class Meta:
#         db_table = "widget_user"
#         verbose_name = "Виджет"
#         verbose_name_plural = "Виджеты"
