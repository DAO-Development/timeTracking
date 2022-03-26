import json
import zipfile

from django.db.models import Sum, F, ExpressionWrapper, FloatField, Q
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from server.serializers import *
from server.test_pdf import *


def check_edit_permissions(request, page):
    user = UserSerializer(request.user)
    group = Group.objects.get(user=user.data["id"])
    functions = GroupFunctions.objects.filter(group_id=group.id).filter(edit=True) \
        .values_list('functions_id__text', flat=True)
    if page in functions:
        return True
    else:
        return False


def check_read_permissions(request, page):
    user = UserSerializer(request.user)
    group = Group.objects.get(user=user.data["id"])
    functions = GroupFunctions.objects.filter(group_id=group.id).filter(read=True) \
        .values_list('functions_id__text', flat=True)
    if page in functions:
        return True
    else:
        return False


def check_admin(request):
    user = UserSerializer(request.user)
    group = Group.objects.get(user=user.data["id"])
    if group.name == "Администраторы":
        return True
    else:
        return False


class MainView(APIView):
    """Статистика для главной страницы"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = UserSerializer(request.user)
        user_profile = UserProfile.objects.get(auth_user_id=user.data["id"]).serializable_value('id')
        news = News.objects.all().count()
        workers = UserProfile.objects.all().count()
        new_workers = UserProfile.objects.filter(create_date=datetime.date.today()).count()
        work_workers = ObjectUser.objects.filter(start_date__lte=datetime.date.today(),
                                                 end_date__gte=datetime.date.today()).count()
        clients = Client.objects.all().count()
        new_clients = Client.objects.filter(create_date=datetime.date.today()).count()
        objects = Objects.objects.all().count()
        work_objects = Objects.objects.filter(date_start__lte=datetime.date.today(),
                                              date_end__gte=datetime.date.today(), active=False).count()
        events = Calendar.objects.all().count()
        start_week = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
        end_week = datetime.date.today() + datetime.timedelta(days=(7 - datetime.date.today().weekday()))
        user_event = Calendar.objects.filter(
            Q(profile=user_profile) | Q(group__in=user.data['groups']) | (Q(group=None) & Q(profile=None)))
        week_events = user_event.filter(start__range=(start_week, end_week)).count()
        today_events = user_event.filter(start=datetime.date.today()).count()
        return Response({"news": news,
                         "workers": {"all": workers, "today": new_workers, "in_work": work_workers},
                         "clients": {"all": clients, "today": new_clients},
                         "objects": {"all": objects, "in_work": work_objects},
                         "calendar": {"all": events, "week": week_events, "today": today_events}
                         })


class UserView(APIView):
    """Пользователи"""
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]

    def get(self, request):
        user = UserSerializer(request.user)
        user_profile = UserProfile.objects.get(auth_user_id=user.data["id"])
        serializer = UserProfileSerializer(user_profile)
        return Response({"data": serializer.data})

    def post(self, request):
        serializer = UserSerializer(data={
            "username": request.data["username"],
            "password": request.data["password"],
            "email": request.data["email"],
        })
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=201)
        else:
            return Response(status=400)

    def put(self, request):
        saved_user = get_object_or_404(User.objects.all(), id=request.data['id'])
        serializer = UserSerializer(saved_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=201)
        else:
            return Response(status=400)

    def delete(self, request):
        user = get_object_or_404(User.objects.all(), email=request.data['email'])
        user.delete()
        return Response(status=204)


class ActiveProfilesView(APIView):
    """Получение списка работников, активные профили"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_profile = UserProfile.objects.all().filter(active=True).order_by('lastname').order_by('name')
        serializer = UserProfileSerializer(user_profile, many=True)
        return Response({"data": serializer.data})


class ProfilesView(APIView):
    """Получение списка работников, профили"""
    permission_classes = [permissions.IsAuthenticated, permissions.AllowAny]

    def get(self, request, id=None):
        if check_read_permissions(request, "Работники"):
            user_profile = UserProfile.objects.all()
            busy = []
            if id is not None:
                user_profile = user_profile.filter(pk=id)
            else:
                user_profile = user_profile.order_by('lastname').order_by('name')
                busy = user_profile.filter(objectuser__end_date__gte=datetime.date.today()).values_list('id', flat=True)
            serializer = UserProfileSerializer(user_profile, many=True)
            return Response({"data": serializer.data, "busy": busy, "cards": CardsUsersSerializer(user_profile[0].cardsusers_set, many=True).data})
        else:
            return Response("Доступ запрещен", status=403)

    def post(self, request):
        serializer = UserProfilePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(create_date=datetime.date.today())
            if request.data["cards"] is not None:
                user_profile = UserProfile.objects.get(auth_user_id=serializer.data["auth_user_id"])
                cards = json.loads(request.data['cards'])
                for card in cards:
                    user_profile.cards.add(Cards.objects.get(pk=card["card"]),
                                           through_defaults={'number': card["number"], "due_date": card["due_date"]})
            return Response({"data": serializer.data}, status=201)
        else:
            return Response(status=400)

    def put(self, request, id=None):
        if check_edit_permissions(request, "Работники"):
            if id is not None:
                name = '/users/' + request.FILES['image'].name
                with open('media' + name, 'wb+') as destination:
                    for chunk in request.FILES['image'].chunks():
                        destination.write(chunk)
                saved_profile = get_object_or_404(UserProfile.objects.all(), id=id)
                serializer = UserProfileSerializer(saved_profile, data={"photo_path": name},
                                                   partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"name": name}, status=201)
                else:
                    return Response("Некорректные данные", status=400)
            saved_profile = get_object_or_404(UserProfile.objects.all(), id=request.data['id'])
            cards = json.loads(request.data['cards'])
            for card in cards:
                if card["id"] == 0:
                    saved_profile.cards.add(Cards.objects.get(pk=card["card"]),
                                            through_defaults={'number': card["number"], "due_date": card["due_date"]})
                else:
                    card = CardsUsers.objects.get(pk=card["id"])
                    card_serializer = CardsUsersSerializer(card, data=card, partial=True)
            serializer = UserProfilePostSerializer(saved_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data": serializer.data, "cards": saved_profile.cards}, status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)


class PrintProfile(APIView):
    """Печать анкеты профиля"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None):
        if check_read_permissions(request, "Работники"):
            user_profile = UserProfile.objects.get(pk=id)
            serializer = UserProfileSerializer(user_profile)
            path = print_profile_form(serializer.data)
            return Response({"path": path}, status=200)
        else:
            return Response("Доступ запрещен", status=403)


class PositionProfileView(APIView):
    """Получение всех существующих специальностей пользователей"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        positions = PositionProfile.objects.all().order_by('name')
        serializer = PositionProfileSerializer(positions, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        if check_admin(request):
            serializer = PositionProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response(status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def delete(self, request):
        if check_admin(request):
            saved_position = get_object_or_404(PositionProfile.objects.all(), id=request.data["id"])
            saved_position.delete()
            return Response(status=204)
        else:
            return Response("Доступ запрещен", status=403)


class CardsView(APIView):
    """Карточки"""
    permission_classes = [permissions.IsAuthenticated, permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        cards = Cards.objects.all()
        serializer = CardsSerializer(cards, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        if check_admin(request):
            serializer = CardsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=200)
            else:
                return Response(status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def put(self, request):
        saved_card = get_object_or_404(Cards.objects.all(), pk=request.data["id"])
        serializer = CardsSerializer(saved_card, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:
            return Response(status=400)

    def delete(self, request):
        saved_card = get_object_or_404(Cards.objects.all(), pk=request.data["id"])
        saved_card.delete()
        return Response(status=204)


class UserDocumentsView(APIView):
    """Документы пользователей"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None):
        if id is None:
            id = UserProfile.objects.get(auth_user_id=UserSerializer(request.user).data["id"]).id
        profile = get_object_or_404(UserProfile.objects.all(), pk=id)
        profile_serializer = UserProfileSerializer(profile)
        documents = UserDocuments.objects.all().filter(user_profile_id=id)
        serializer = UserDocumentsSerializer(documents, many=True)
        return Response({"profile": profile_serializer.data, "documents": serializer.data}, status=200)

    def put(self, request):
        # todo Сделать чтобы пользователь добавлял документы только для себя,
        # либо проверка прав редактирования
        create_date = datetime.date.today()
        name = ''
        if len(request.FILES) == 1:
            name = '/documents/' + request.FILES['document'].name
            with open('media' + name, 'wb+') as destination:
                for chunk in request.FILES['document'].chunks():
                    destination.write(chunk)
        else:
            name = request.data['path']
        data = {
            "user_profile_id": int(request.data['user_profile_id']),
            "name": request.data['name'],
            "create_date": create_date,
            "path": name,
        }
        if request.data["id"] == "0":
            serializer = UserDocumentsSerializer(data=data)
        else:
            saved_object = get_object_or_404(UserDocuments.objects.all(), id=request.data["id"])
            serializer = UserDocumentsSerializer(saved_object, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response("Некорректные данные", status=400)

    def delete(self, request):
        # todo удаление только своих или с правами редактирования
        document = get_object_or_404(UserDocuments.objects.all(), id=request.data["id"])
        document.delete()
        return Response(status=204)


class UserGroupsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        if check_admin(request):
            user = User.objects.get(pk=request.data['auth_user_id'])
            user.groups.clear()
            user.groups.add(request.data['group_id'])
            return Response({"data": user.groups.all().values_list('name', flat=True)})
        else:
            return Response("Доступ запрещен", status=403)


class GroupView(APIView):
    """Группа пользователя"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = UserSerializer(request.user)
        group = Group.objects.get(user=user.data["id"])
        admin = False
        if (group.name == "Администраторы"):
            admin = True
        functions = GroupFunctions.objects.filter(group_id=group.id)
        read = []
        edit = []
        for func in functions:
            if func.read:
                read.append(Functions.objects.get(pk=func.functions_id.id).text)
            if func.edit:
                edit.append(Functions.objects.get(id=func.functions_id.id).text)
        return Response({"read": read, "edit": edit, "admin": admin})

    def put(self, request):
        if check_admin(request):
            saved_group = get_object_or_404(Group.objects.all(), pk=request.data['id'])
            serializer = GroupSerializer(saved_group, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def post(self, request):
        if check_admin(request):
            serializer = GroupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def delete(self, request):
        if check_admin(request):
            group = get_object_or_404(Group.objects.all(), id=request.data['id'])
            group.delete()
            return Response(status=204)
        else:
            return Response("Доступ запрещен", status=403)


class GroupsView(APIView):
    """Группы"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        functions = Functions.objects.all()
        data = {}
        for group in groups:
            data.update({group.name: {}})
            for function in functions:
                children = GroupFunctions.objects.filter(group_id=group.id, functions_id=function.id)
                if len(children) == 1:
                    children = GroupFunctions.objects.get(group_id=group.id, functions_id=function.id)
                    children_serializer = GroupFunctionsSerializer(children)
                    data[group.name].update({function.text: {"name": function.text,
                                                             "data": children_serializer.data}})
                else:
                    data[group.name].update({function.text: {"name": function.text,
                                                             "data": {"id": 0,
                                                                      "group_id": group.id,
                                                                      "functions_id": function.id,
                                                                      "read": False,
                                                                      "edit": False}}})
        return Response({"groups": serializer.data, "functions": data})


class GroupFunctionsView(APIView):
    """Функции групп"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if check_admin(request):
            functions = GroupFunctions.objects.all()
            serializer = GroupFunctionsSerializer(functions, many=True)
            return Response({"data": serializer.data})
        else:
            return Response("Доступ запрещен", status=403)

    def put(self, request):
        if check_admin(request):
            if request.data["id"] == "0":
                serializer = GroupFunctionsSerializer(data=request.data)
            else:
                saved_function = get_object_or_404(GroupFunctions.objects.all(), id=request.data["id"])
                serializer = GroupFunctionsSerializer(saved_function, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"id": serializer.data["id"]}, status=201)
            else:
                return Response(status=400)
        else:
            return Response("Доступ запрещен", status=403)


class NewsView(APIView):
    """Новости"""
    permission_classes = [permissions.AllowAny]

    def get(self, request, id=None):
        news = News.objects.all()
        if id is not None:
            news = news.filter(pk=id)
        serializer = NewsSerializer(news, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        name = ''
        if len(request.FILES) == 1:
            name = '/news/' + request.FILES['image'].name
            with open('media' + name, 'wb+') as destination:
                for chunk in request.FILES['image'].chunks():
                    destination.write(chunk)
        serializer = NewsSerializer(data={
            "title": request.data["title"],
            "text": request.data["text"],
            "photo_path": name,
            "create_date": datetime.date.today()
        })
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def put(self, request):
        saved_news = get_object_or_404(News.objects.all(), id=request.data["id"])
        serializer = NewsSerializer(saved_news, data={
            "title": request.data["title"],
            "text": request.data["text"]
        }, partial=True)
        if len(request.FILES) == 1:
            name = '/news/' + request.FILES['image'].name
            with open('media' + name, 'wb+') as destination:
                for chunk in request.FILES['image'].chunks():
                    destination.write(chunk)
            serializer = NewsSerializer(saved_news, data={
                "title": request.data["title"],
                "text": request.data["text"],
                "photo_path": name
            }, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request):
        news = get_object_or_404(News.objects.all(), id=request.data["id"])
        news.delete()
        return Response(status=204)


class ObjectsView(APIView):
    """Объекты"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Objects.objects.all()

    def get(self, request, client_id=None):
        if check_read_permissions(request, "Объекты"):
            user = UserSerializer(request.user)
            objects = Objects.objects.all()
            if client_id is not None:
                objects = objects.filter(client_id=client_id)
            if not check_admin(request):
                user_profile = UserProfileSerializer(UserProfile.objects.get(auth_user_id=user.data["id"]))
                objects_user = ObjectUser.objects.filter(user_profile_id=user_profile.data["id"]).values_list(
                    'objects_id',
                    flat=True)
                objects = objects.filter(pk__in=objects_user)
            serializer = ObjectsSerializer(objects, many=True)
            return Response({"data": serializer.data})
        else:
            return Response("Доступ запрещен", status=403)

    def post(self, request):
        if check_edit_permissions(request, "Объекты"):
            serializer = ObjectsPostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(create_date=datetime.date.today())
                return Response(status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def put(self, request, client_id=None):  # client_id -- id
        if check_edit_permissions(request, "Объекты"):
            serializer = None
            if client_id is not None:
                name = '/objects/' + request.FILES['image'].name
                with open('media' + name, 'wb+') as destination:
                    for chunk in request.FILES['image'].chunks():
                        destination.write(chunk)
                saved_object = get_object_or_404(Objects.objects.all(), id=client_id)
                serializer = ObjectsSerializer(saved_object, data={"photo_path": name},
                                               partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"name": name}, status=201)
                else:
                    return Response("Некорректные данные", status=400)
            else:
                saved_object = get_object_or_404(Objects.objects.all(), id=request.data["id"])
                serializer = ObjectsSerializer(saved_object, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=201)
                else:
                    return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def delete(self, request):
        if check_edit_permissions(request, "Объекты"):
            object = get_object_or_404(Objects.objects.all(), id=request.data["id"])
            object.delete()
            return Response(status=204)
        else:
            return Response("Доступ запрещен", status=403)


class ObjectUserView(APIView):
    """Рабочие на объектах"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, objects_id=None):
        if check_read_permissions(request, "Объекты"):
            if objects_id is not None:
                workers = ObjectUser.objects.all().filter(objects_id=objects_id)
                serializer = ObjectUserSerializer(workers, many=True)
            else:
                busy = ObjectUser.objects.all().filter(end_date__gt=datetime.date.today()).values_list(
                    'user_profile_id',
                    flat=True)
                workers = UserProfile.objects.all().exclude(id__in=busy)
                serializer = UserProfileSerializer(workers, many=True)
            return Response({"data": serializer.data})
        else:
            return Response("Доступ запрещен", status=403)

    def put(self, request):
        if check_edit_permissions(request, "Объекты"):
            if request.data["id"] == "0":
                end_date = request.data['end_date']
                if request.data['end_date'] == "":
                    end_date = None
                serializer = ObjectUserPostSerializer(data={
                    "user_profile_id": int(request.data['user_profile_id']),
                    "objects_id": int(request.data['objects_id']),
                    "start_date": request.data['start_date'],
                    "end_date": end_date,
                    "comment": request.data['comment'],
                })
            else:
                saved_object = get_object_or_404(ObjectUser.objects.all(), id=request.data["id"])
                serializer = ObjectUserSerializer(saved_object, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def delete(self, request):
        if check_edit_permissions(request, "Объекты"):
            object_user = get_object_or_404(ObjectUser.objects.all(), id=request.data['id'])
            object_user.delete()
            return Response(status=204)
        else:
            return Response("Доступ запрещен", status=403)


class ObjectPhotoView(APIView):
    """Фото объектов"""
    # todo нужен ли вообще?
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, objects_id):
        object_photo = ObjectPhoto.objects.filter(objects_id=objects_id)
        serializer = ObjectPhotoSerializer(object_photo, many=True)
        return Response({"data": serializer.data})

    def put(self, request):
        if request.data['id'] != '':
            saved_object = ObjectPhoto.objects.get(pk=request.data['id'])
            serializer = ObjectPhoto(saved_object, data=request.data, partial=True)
        else:
            serializer = ObjectPhotoSerializer(data={
                "photo_path": request.data['photo_path'],
                "objects_id": request.data['objects_id'],
            })
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request, id):
        object_photo = get_object_or_404(ObjectPhoto.objects.all(), id=id)
        object_photo.delete()
        return Response(status=204)


class ObjectCommentsView(APIView):
    """Комментарии к объектам"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None):
        user = UserSerializer(request.user)
        user_profile = UserProfile.objects.get(auth_user_id=user.data["id"]).serializable_value('id')
        comments = ObjectComments.objects.all()
        if id is not None:
            comments = comments.filter(objects_id=id).filter(object_comments_id__isnull=True)
        data = {}
        for com in comments:
            children = ObjectComments.objects.filter(object_comments_id=com.id)
            children_serializer = ObjectCommentsSerializer(children, many=True)
            data.update({com.id: children_serializer.data})
        serializer = ObjectCommentsSerializer(comments, many=True)
        return Response({"profile": user_profile, "comments": serializer.data, "data": data})

    def post(self, request):
        user = UserSerializer(request.user)
        user_profile = UserProfile.objects.get(auth_user_id=user.data["id"]).serializable_value('id')
        object_comments_id = request.data['object_comments_id']
        serializer = ObjectCommentsPostSerializer(data={
            'text': request.data['text'],
            'object_comments_id': object_comments_id,
            'user_profile_id': user_profile,
            'objects_id': request.data['objects_id']
        })
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request, id):
        object_comment = get_object_or_404(ObjectComments.objects.all(), id=id)
        object_comment.delete()
        return Response(status=204)


class ClientView(APIView):
    """Клиенты"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None):
        if check_read_permissions(request, "Клиенты"):
            clients = Client.objects.all().order_by('name')
            if id is not None:
                clients = clients.filter(pk=id)
            serializer = ClientSerializer(clients, many=True)
            return Response({"data": serializer.data})
        else:
            return Response("Доступ запрещен", status=403)

    def post(self, request):
        if check_edit_permissions(request, 'Клиенты'):
            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(create_date=datetime.date.today())
                return Response(status=201)
            else:
                return Response("Неверные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def put(self, request):
        if check_edit_permissions(request, 'Клиенты'):
            saved_client = get_object_or_404(Client.objects.all(), id=request.data["id"])
            data = request.data
            if len(request.FILES) == 1:
                name = '/clients/' + request.FILES['image'].name
                with open('media' + name, 'wb+') as destination:
                    for chunk in request.FILES['image'].chunks():
                        destination.write(chunk)
                data = {"logo_path": name}
            serializer = ClientSerializer(saved_client, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response("Неверные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def delete(self, request):
        if check_edit_permissions(request, 'Клиенты'):
            saved_client = get_object_or_404(Client.objects.all(), id=request.data["id"])
            saved_client.delete()
            return Response(status=204)
        else:
            return Response("Доступ запрещен", status=403)


class ClientCommentsView(APIView):
    """Комментарии к клиентам"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None):
        if check_read_permissions(request, "Клиенты"):
            user = UserSerializer(request.user)
            user_profile = UserProfile.objects.get(auth_user_id=user.data["id"]).serializable_value('id')
            comments = ClientComments.objects.all()
            if id is not None:
                comments = comments.filter(client=id).filter(client_comments__isnull=True)
            data = {}
            for com in comments:
                children = ClientComments.objects.filter(client_comments=com.id)
                children_serializer = ClientCommentsSerializer(children, many=True)
                data.update({com.id: children_serializer.data})
            serializer = ClientCommentsSerializer(comments, many=True)
            return Response({"profile": user_profile, "comments": serializer.data, "data": data})
        else:
            return Response("Доступ запрещен", status=403)

    def post(self, request):
        if check_read_permissions(request, "Клиенты"):
            user = UserSerializer(request.user)
            user_profile = UserProfile.objects.get(auth_user_id=user.data["id"]).serializable_value('id')
            serializer = ClientCommentsPostSerializer(data={
                'text': request.data['text'],
                'client_comments': request.data['client_comments'],
                'user_profile': user_profile,
                'client': request.data['client']
            })
            # return Response(request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def delete(self, request):
        if check_read_permissions(request, "Клиенты"):
            comment = get_object_or_404(ClientComments.objects.all(), id=request.data["id"])
            comment.delete()
            return Response(status=204)
        else:
            return Response("Доступ запрещен", status=403)


class ClientBranchesView(APIView):
    """Получение всех существующих отраслей клиентов"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        branches = Client.objects.all().values_list('branch', flat=True).distinct('branch').order_by('branch')
        return Response({"branches": branches})


class ClientEmployeesView(APIView):
    """Сотрудники фирм-клиентов"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None, idclient=None):
        if check_read_permissions(request, "Контакты"):
            employees = ClientEmployees.objects.all().order_by('lastname', 'name')
            if idclient is not None:
                employees = employees.filter(client_id=idclient).order_by('lastname', 'name')
            if id is not None:
                employees = employees.filter(pk=id)
            else:
                if request.GET['client'] != "Все":
                    employees = employees.filter(client=request.GET['client'])
                if request.GET['position'] != "Все":
                    employees = employees.filter(position=request.GET["position"])

            serializer = ClientEmployeesSerializer(employees, many=True)
            return Response({"data": serializer.data})
        else:
            return Response("Доступ запрещен", status=403)

    def post(self, request):
        if check_edit_permissions(request, "Контакты"):
            serializer = ClientEmployeesPostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def put(self, request):
        if check_edit_permissions(request, "Контакты"):
            saved_employee = get_object_or_404(ClientEmployees.objects.all(), id=request.data["id"])
            data = request.data
            if len(request.FILES) == 1:
                name = '/contacts/' + request.FILES['image'].name
                with open('media' + name, 'wb+') as destination:
                    for chunk in request.FILES['image'].chunks():
                        destination.write(chunk)
                data = {"photo_path": name}
            serializer = ClientEmployeesPostSerializer(saved_employee, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def delete(self, request):
        if check_edit_permissions(request, "Контакты"):
            saved_employee = get_object_or_404(ClientEmployees.objects.all(), id=request.data["id"])
            saved_employee.delete()
            return Response(status=204)
        else:
            return Response("Доступ запрещен", status=403)


class PositionClientView(APIView):
    """Получение всех существующих должностей в штатах фирм-клиентов"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        positions = PositionClient.objects.all().order_by('name')
        serializer = PositionClientSerializer(positions, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        if check_admin(request):
            serializer = PositionClientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def delete(self, request):
        if check_admin(request):
            saved_position = get_object_or_404(PositionClient.objects.all(), id=request.data["id"])
            saved_position.delete()
            return Response(status=204)
        else:
            return Response("Доступ запрещен", status=403)


class ContactCommentsView(APIView):
    """Комментарии к контактам"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None):
        if check_read_permissions(request, "Контакты"):
            user = UserSerializer(request.user)
            user_profile = UserProfile.objects.get(auth_user_id=user.data["id"]).serializable_value('id')
            comments = ContactComments.objects.all()
            if id is not None:
                comments = comments.filter(contact=id).filter(contact_comments__isnull=True)
            data = {}
            for com in comments:
                children = ContactComments.objects.filter(contact_comments=com.id)
                children_serializer = ContactCommentsSerializer(children, many=True)
                data.update({com.id: children_serializer.data})
            serializer = ContactCommentsSerializer(comments, many=True)
            return Response({"profile": user_profile, "comments": serializer.data, "data": data})
        else:
            return Response("Доступ запрещен", status=403)

    def post(self, request):
        if check_read_permissions(request, "Контакты"):
            user = UserSerializer(request.user)
            user_profile = UserProfile.objects.get(auth_user_id=user.data["id"]).serializable_value('id')
            serializer = ContactCommentsPostSerializer(data={
                'text': request.data['text'],
                'contact_comments': request.data['contact_comments'],
                'user_profile': user_profile,
                'contact': request.data['contact']
            })
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def delete(self, request):
        if check_read_permissions(request, "Контакты"):
            comment = get_object_or_404(ContactComments.objects.all(), id=request.data["id"])
            comment.delete()
            return Response(status=204)
        else:
            return Response("Доступ запрещен", status=403)


class NotesView(APIView):
    """Виджет-блокнот"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notes = Notes.objects.filter(user=UserSerializer(request.user).data['id'])
        serializer = NotesSerializer(notes, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        serializer = NotesSerializer(data={
            "text": request.data['text'],
            "color": request.data['color'],
            "user": UserSerializer(request.user).data['id'],
            "last_save": datetime.datetime.now()
        })
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def put(self, request):
        saved_note = get_object_or_404(Notes.objects.all(), id=request.data["id"])
        serializer = NotesSerializer(saved_note, data={
            "text": request.data['text'],
            "color": request.data['color'],
            "last_save": request.data['last_save']
        }, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request):
        saved_note = get_object_or_404(Notes.objects.all(), id=request.data["id"])
        saved_note.delete()
        return Response(status=204)


class ChequeCategoryView(APIView):
    """Все категории чеков"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        categories = ChequeCategory.objects.all().order_by('name')
        serializer = ChequeCategorySerializer(categories, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        if check_admin(request):
            serializer = ChequeCategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def delete(self, request):
        if check_admin(request):
            saved_category = get_object_or_404(ChequeCategory.objects.all(), id=request.data["id"])
            saved_category.delete()
            return Response(status=204)
        else:
            return Response("Доступ запрещен", status=403)


class TermView(APIView):
    """Сроки для счетов и предложений"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        terms = Term.objects.all().order_by('days')
        serializer = TermSerializer(terms, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        if check_admin(request):
            serializer = TermSerializer(data={"days": request.data['name']})
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def delete(self, request):
        if check_admin(request):
            saved_term = get_object_or_404(Term.objects.all(), id=request.data["id"])
            saved_term.delete()
            return Response(status=204)
        else:
            return Response("Доступ запрещен", status=403)


class TaxView(APIView):
    """Налог для бухгалтерии"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        taxes = Tax.objects.all().order_by('tax')
        serializer = TaxSerializer(taxes, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        if check_admin(request):
            serializer = TaxSerializer(data={"tax": request.data['name']})
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def delete(self, request):
        if check_admin(request):
            saved_term = get_object_or_404(Tax.objects.all(), id=request.data["id"])
            saved_term.delete()
            return Response(status=204)
        else:
            return Response("Доступ запрещен", status=403)


class PurchasesView(APIView):
    """Покупки"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None):
        if check_read_permissions(request, "Бухгалтерия"):
            purchases = Purchases.objects.order_by('date')
            photos = {}
            statistic = {}
            if id is not None:
                purchases = purchases.filter(id=id)
            elif 'year' in request.GET:
                purchases = purchases.filter(date__year=request.GET['year'],
                                             date__month=request.GET['month'])
                statistic.update({'count_categories': Purchases.objects.filter(date__year=request.GET['year'],
                                                                               date__month=request.GET['month']) \
                                 .values('category').distinct().count()})
                statistic.update({'by_categories': Purchases.objects.filter(date__year=request.GET['year'],
                                                                            date__month=request.GET['month']) \
                                 .values('category__name').annotate(Sum('price'))})
                statistic.update({'sum': Purchases.objects.filter(date__year=request.GET['year'],
                                                                  date__month=request.GET['month'])
                                 .aggregate(Sum('price'))['price__sum']})
                for item in purchases:
                    docs = ChequeDocuments.objects.filter(purchases=item.id).order_by('id')
                    docs_serializer = ChequeDocumentsSerializer(docs, many=True)
                    photos.update({item.id: docs_serializer.data})
            serializer = PurchasesSerializer(purchases, many=True)
            return Response({"data": serializer.data,
                             "photos": photos,
                             "statistic": statistic})
        else:
            return Response("Доступ запрещен", status=403)

    def post(self, request):
        if check_edit_permissions(request, "Бухгалтерия"):
            serializer = PurchasesPostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"id": serializer.data['id']}, status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def put(self, request):
        if check_edit_permissions(request, "Бухгалтерия"):
            saved = get_object_or_404(Purchases.objects.all(), id=request.data["id"])
            serializer = PurchasesPostSerializer(saved, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response(status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def delete(self, request):
        if check_edit_permissions(request, "Бухгалтерия"):
            saved = get_object_or_404(Purchases.objects.all(), id=request.data["id"])
            saved.delete()
            return Response(status=204)
        else:
            return Response("Доступ запрещен", status=403)


class SalesView(APIView):
    """Продажи"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None):
        if check_read_permissions(request, "Бухгалтерия"):
            sales = Sales.objects.all()
            photos = {}
            items = {}
            statistic = {}
            if id is not None:
                sales = sales.filter(id=id)
            elif 'year' in request.GET:
                sales = sales.filter(create_date__year=request.GET['year'],
                                     create_date__month=request.GET['month'])
                statistic.update({'count_clients': Sales.objects.filter(create_date__year=request.GET['year'],
                                                                        create_date__month=request.GET['month']) \
                                 .values('client').distinct().count()})
                statistic.update({'sum': Sales.objects.filter(create_date__year=request.GET['year'],
                                                              create_date__month=request.GET['month']) \
                                 .aggregate(sum=Sum(F('items__price') * F('items__quantity')))['sum']})
                statistic.update({'sum_tax': Sales.objects.filter(create_date__year=request.GET['year'],
                                                                  create_date__month=request.GET['month']) \
                                 .aggregate(
                    sum=ExpressionWrapper(Sum(F('items__price') * (100 + F('items__tax')) / 100 * F('items__quantity')),
                                          output_field=FloatField()))['sum']})
            for item in sales:
                serializer = SalesSerializer(item)
                docs = ChequeDocuments.objects.filter(sales=item.id).order_by('id')
                docs_serializer = ChequeDocumentsSerializer(docs, many=True)
                photos.update({item.id: docs_serializer.data})
                things = Items.objects.filter(pk__in=serializer.data['items']).order_by('id')
                things_serializer = ItemsSerializer(things, many=True)
                items.update({item.id: things_serializer.data})
            serializer = SalesSerializer(sales, many=True)
            return Response({"data": serializer.data,
                             "photos": photos,
                             "items": items,
                             "statistic": statistic})
        else:
            return Response("Доступ запрещен", status=403)

    def post(self, request):
        if check_edit_permissions(request, "Бухгалтерия"):
            items = json.loads(request.data['items'])
            serializer = SalesPostSerializer(data={
                'id': request.data['id'],
                'create_date': request.data['create_date'],
                'object_number': request.data['object_number'],
                'client': request.data['client'],
                'object': request.data['object'],
                'payment_terms': request.data['payment_terms'],
                'number_link': request.data['number_link'],
                'comment': request.data['comment'],
                'description': request.data['description'],
            })
            if serializer.is_valid():
                serializer.save()
                sale = Sales.objects.get(pk=serializer.data['id'])
                for item in items:
                    sale.items.create(name=item['name'], price=item['price'], tax=item['tax'],
                                      discount=item['discount'], quantity=item['quantity'],
                                      measurement=item['measurement'])
                return Response({"id": serializer.data['id']}, status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def put(self, request):
        if check_edit_permissions(request, "Бухгалтерия"):
            saved = get_object_or_404(Sales.objects.all(), id=request.data["id"])
            serializer = SalesPostSerializer(saved, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                items = json.loads(request.data['items'])
                sale = Sales.objects.get(pk=serializer.data['id'])
                for item in items:
                    if 'id' not in item:
                        sale.items.create(name=item['name'], price=item['price'], tax=item['tax'],
                                          discount=item['discount'], quantity=item['quantity'],
                                          measurement=item['measurement'])
                return Response(status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def delete(self, request):
        if check_edit_permissions(request, "Бухгалтерия"):
            saved = get_object_or_404(Sales.objects.all(), id=request.data["id"])
            saved.delete()
            return Response(status=204)
        else:
            return Response("Доступ запрещен", status=403)


class PrintSalesView(APIView):

    def get(self, request, id=None):
        if check_read_permissions(request, "Бухгалтерия"):
            sale = Sales.objects.get(pk=id)
            serializer = SalesSerializer(sale)
            items = Items.objects.filter(pk__in=serializer.data['items']).order_by('id')
            items_serializer = ItemsSerializer(items, many=True)
            path = print_sale(serializer.data, items_serializer.data)
            return Response({"path": path}, status=200)
        else:
            return Response("Доступ запрещен", status=403)


class ChequeDocumentsView(APIView):
    """Фото чеков"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        documents = ChequeDocuments.objects.all()
        serializer = ChequeDocumentsSerializer(documents, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        if len(request.FILES) >= 0:
            for i in range(1, len(request.FILES) + 1):
                name = '/cheque/' + request.FILES['document' + str(i)].name
                with open('media' + name, 'wb+') as destination:
                    for chunk in request.FILES['document' + str(i)].chunks():
                        destination.write(chunk)
                data = {
                    "path": name,
                    "sales": request.data['sales'],
                    "purchases": request.data['purchases'],
                }
                serializer = ChequeDocumentsSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(status=400)
        return Response(status=201)

    def delete(self, request):
        saved = get_object_or_404(ChequeDocuments.objects.all(), id=request.data["id"])
        saved.delete()
        return Response(status=204)


class DocumentsAccountingView(APIView):
    """Документы бухгалтерии"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, mode_id, id=None):
        if check_read_permissions(request, "Бухгалтерия"):
            documents = DocumentsAccounting.objects.all().filter(mode=mode_id)
            if id is not None:
                documents = documents.filter(pk=id)
            serializer = DocumentsAccountingSerializer(documents, many=True)
            return Response({"data": serializer.data})
        else:
            return Response("Доступ запрещен", status=403)

    def put(self, request, mode_id):
        if check_edit_permissions(request, "Бухгалтерия"):
            path = ''
            if len(request.FILES) >= 0:
                for i in range(1, len(request.FILES) + 1):
                    name = '/accounting/' + request.FILES['document' + str(i)].name
                    with open('media' + name, 'wb+') as destination:
                        for chunk in request.FILES['document' + str(i)].chunks():
                            destination.write(chunk)
                    path += name
                    if i != len(request.FILES):
                        path += ';'
            else:
                path = request.data['path']
            data = {
                "name": request.data['name'],
                "create_date": request.data['create_date'],
                "path": path,
                "mode": mode_id,
            }
            if request.data["id"] == "0":
                serializer = DocumentsAccountingSerializer(data=data)
            else:
                saved = get_object_or_404(DocumentsAccounting.objects.all(), id=request.data["id"])
                serializer = DocumentsAccountingSerializer(saved, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def delete(self, request):
        if check_edit_permissions(request, "Бухгалтерия"):
            saved = get_object_or_404(DocumentsAccounting.objects.all(), id=request.data["id"])
            # @todo сделать удаление файлов
            # path = saved.path
            # path = path.split(";")
            # return Response({"data": path})
            # for item in path:
            #     del_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "/media" + item)
            #     os.remove(del_path)
            saved.delete()
            return Response(status=204)
        else:
            return Response("Доступ запрещен", status=403)


class DocumentsClientView(APIView):
    """Документы бухгалтерии с клиентами"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, mode_id, id=None):
        if check_read_permissions(request, "Бухгалтерия"):
            documents = DocumentsClient.objects.all().filter(mode=mode_id)
            if id is not None:
                documents = documents.filter(pk=id)
            serializer = DocumentsClientSerializer(documents, many=True)
            return Response({"data": serializer.data})
        else:
            return Response("Доступ запрещен", status=403)

    def put(self, request, mode_id):
        if check_edit_permissions(request, "Бухгалтерия"):
            path = ''
            if len(request.FILES) >= 0:
                for i in range(1, len(request.FILES) + 1):
                    name = '/accounting/clients/' + request.FILES['document' + str(i)].name
                    with open('media' + name, 'wb+') as destination:
                        for chunk in request.FILES['document' + str(i)].chunks():
                            destination.write(chunk)
                    path += name
                    if i != len(request.FILES):
                        path += ';'
            else:
                path = request.data['path']
            data = {
                "name": request.data['name'],
                "create_date": request.data['create_date'],
                "path": path,
                "client": request.data['client'],
                "mode": mode_id,
            }
            if request.data["id"] == "0":
                serializer = DocumentsClientPostSerializer(data=data)
            else:
                saved = get_object_or_404(DocumentsClient.objects.all(), id=request.data["id"])
                serializer = DocumentsClientPostSerializer(saved, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def delete(self, request):
        if check_edit_permissions(request, "Бухгалтерия"):
            saved = get_object_or_404(DocumentsClient.objects.all(), id=request.data["id"])
            saved.delete()
            return Response(status=204)
        else:
            return Response("Доступ запрещен", status=403)


class WaybillGoalView(APIView):
    """Цели для путевых листов"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        goals = WaybillGoal.objects.all()
        serializer = WaybillGoalSerializer(goals, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        if check_admin(request):
            serializer = WaybillGoalSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def delete(self, request):
        if check_admin(request):
            saved = get_object_or_404(WaybillGoal.objects.all(), id=request.data["id"])
            saved.delete()
            return Response(status=204)
        else:
            return Response("Доступ запрещен", status=403)


class WaybillView(APIView):
    """Путевые листы"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None):
        if id is not None:
            waybills = Waybill.objects.all().filter(pk=id)
        else:
            user = UserSerializer(request.user)
            user_profile = UserProfile.objects.get(auth_user_id=user.data["id"]).serializable_value('id')
            waybills = Waybill.objects.all().order_by('-date_start', '-time_start')
            if 1 not in user.data['groups']:
                waybills = waybills.filter(user_profile=user_profile)
            else:
                if request.GET['place'] != "Все":
                    waybills = waybills.filter(
                        Q(departure=request.GET['place']) | Q(destination=request.GET['place']))
                if request.GET['worker'] != "Все":
                    waybills = waybills.filter(user_profile=request.GET["worker"])
        serializer = WaybillSerializer(waybills, many=True)
        places = list(Waybill.objects.all().values_list('departure', flat=True).distinct())
        for item in list(Waybill.objects.all().values_list('destination', flat=True).distinct()):
            if item not in places:
                places.append(item)
        return Response({"data": serializer.data, "places": places})

    def post(self, request):
        user = UserSerializer(request.user)
        user_profile = UserProfile.objects.get(auth_user_id=user.data["id"]).serializable_value('id')
        serializer = WaybillPostSerializer(data={
            'date_start': request.data['date_start'],
            'date_end': request.data['date_end'],
            'departure': request.data['departure'],
            'destination': request.data['destination'],
            'kilometrage_start': request.data['kilometrage_start'],
            'kilometrage_end': request.data['kilometrage_end'],
            'time_start': request.data['time_start'],
            'time_end': request.data['time_end'],
            'goal': request.data['goal'],
            'auto_mark': request.data['auto_mark'],
            'auto_type': request.data['auto_type'],
            'auto_fuel': request.data['auto_fuel'],
            'user_profile': user_profile
        })
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def put(self, request):
        saved = get_object_or_404(Waybill.objects.all(), id=request.data["id"])
        serializer = WaybillPostSerializer(saved, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request):
        saved = get_object_or_404(Waybill.objects.all(), id=request.data["id"])
        saved.delete()
        return Response(status=204)


class OfferView(APIView):
    """Предложения"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None):
        if check_read_permissions(request, "Бухгалтерия"):
            offers = Offer.objects.all()
            items = {}
            if id is not None:
                offers = offers.filter(id=id)
            else:
                if request.GET['active'] != "Все":
                    if request.GET['active'] == "true":
                        offers = offers.filter(active=True)
                    else:
                        offers = offers.filter(active=False)
                if request.GET['client'] != "Все":
                    offers = offers.filter(client=request.GET["client"])
            for item in offers:
                serializer = OfferSerializer(item)
                things = Items.objects.filter(pk__in=serializer.data['items']).order_by('id')
                things_serializer = ItemsSerializer(things, many=True)
                items.update({item.id: things_serializer.data})
            serializer = OfferSerializer(offers, many=True)
            return Response({"data": serializer.data, "items": items})
        else:
            return Response("Доступ запрещен", status=403)

    def post(self, request):
        if check_edit_permissions(request, "Бухгалтерия"):
            user = UserSerializer(request.user)
            user_profile = UserProfile.objects.get(auth_user_id=user.data["id"]).serializable_value('id')
            items = json.loads(request.data['items'])
            serializer = OfferPostSerializer(data={
                'author': user_profile,
                'create_date': request.data["create_date"],
                'active': request.data["active"],
                'term': request.data["term"],
                'client': request.data["client"],
                'object': request.data["object"],
                'contact': request.data["contact"],
                'from_client': request.data["from_client"]
            })
            if serializer.is_valid():
                serializer.save()
                offer = Offer.objects.get(pk=serializer.data['id'])
                for item in items:
                    offer.items.create(name=item['name'], price=item['price'], tax=item['tax'],
                                       discount=item['discount'], type=item['type'],
                                       quantity=item['quantity'], measurement=item['measurement'])
                return Response(status=201)
            else:
                return Response("Некоррекные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def put(self, request):
        if check_edit_permissions(request, "Бухгалтерия"):
            saved = get_object_or_404(Offer.objects.all(), id=request.data["id"])
            serializer = OfferPostSerializer(saved, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                items = json.loads(request.data['items'])
                offer = Offer.objects.get(pk=serializer.data['id'])
                for item in items:
                    if 'id' not in item:
                        offer.items.create(name=item['name'], price=item['price'], tax=item['tax'],
                                           discount=item['discount'], quantity=item['quantity'],
                                           measurement=item['measurement'])
                return Response(status=201)
            else:
                return Response("Некорректные данные", status=400)
        else:
            return Response("Доступ запрещен", status=403)

    def delete(self, request):
        if check_edit_permissions(request, "Бухгалтерия"):
            saved = get_object_or_404(Offer.objects.all(), id=request.data["id"])
            saved.delete()
            return Response(status=204)
        else:
            return Response("Доступ запрещен", status=403)


class PrintOfferView(APIView):

    def get(self, request, id=None):
        if check_read_permissions(request, "Бухгалтерия"):
            offer = Offer.objects.get(pk=id)
            serializer = OfferSerializer(offer)
            items = Items.objects.filter(pk__in=serializer.data['items']).order_by('type', 'id')
            items_serializer = ItemsSerializer(items, many=True)
            # return Response({"offer": serializer.data, "items": items_serializer.data})
            path = print_offer(serializer.data, items_serializer.data)
            return Response({"path": path}, status=200)
        else:
            return Response("Доступ запрещен", status=403)


class ItemsView(APIView):
    """Товары и услуги"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = Items.objects.all()
        serializer = ItemsSerializer(items, many=True)
        return Response({"data": serializer.data})

    def put(self, request):
        saved = get_object_or_404(Items.objects.all(), id=request.data["id"])
        serializer = ItemsSerializer(saved, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request):
        saved = get_object_or_404(Items.objects.all(), id=request.data["id"])
        if 'sale_id' in request.data:
            sale = Sales.objects.get(pk=request.data['sale_id'])
            sale.items.remove(saved)
        elif 'offer_id' in request.data:
            offer = Offer.objects.get(pk=request.data['offer_id'])
            offer.items.remove(saved)
        saved.delete()
        return Response(status=204)


class CalendarView(APIView):
    """Календарь"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = UserSerializer(request.user)
        user_profile = UserProfile.objects.get(auth_user_id=user.data["id"]).serializable_value('id')
        events = Calendar.objects.all()
        edit_event = events.filter(author=user_profile)
        user_event = events.filter(
            Q(profile=user_profile) | Q(group__in=user.data['groups']) | (Q(group=None) & Q(
                profile=None))).exclude(author=user_profile)
        serializer_edit = CalendarSerializer(edit_event, many=True)
        serializer = CalendarSerializer(user_event, many=True)
        return Response({"data": serializer.data, "edit": serializer_edit.data})

    def post(self, request):
        user = UserSerializer(request.user)
        user_profile = UserProfile.objects.get(auth_user_id=user.data["id"]).serializable_value('id')
        data = {
            "author": user_profile,
            "group": request.data["group"],
            "profile": request.data["profile"],
            "name": request.data["name"],
            "start": request.data["start"],
            "end": request.data["end"],
            "allDay": request.data["allDay"],
            "color": request.data["color"],
            "description": request.data["description"]
        }
        if request.data["self"]:
            data["profile"] = user_profile
            data["group"] = None
        if request.data["end"] == '':
            data["end"] = None
        serializer = CalendarSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def put(self, request):
        saved = get_object_or_404(Calendar.objects.all(), id=request.data["id"])
        serializer = CalendarSerializer(saved, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request):
        saved = get_object_or_404(Calendar.objects.all(), id=request.data["id"])
        saved.delete()
        return Response(status=204)


class TimeReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_profile_id=None):
        reports = TimeReport.objects.all()
        if user_profile_id is None:
            user = UserSerializer(request.user)
            user_profile = UserProfile.objects.get(auth_user_id=user.data["id"]).serializable_value('id')
            reports = reports.filter(user_profile_id=user_profile)
        elif user_profile_id != "all":
            reports = reports.filter(user_profile_id=user_profile_id)
        serializer = TimeReportSerializer(reports, many=True)
        return Response({"data": serializer.data}, status=200)

    def post(self, request):
        user = UserSerializer(request.user)
        user_profile = UserProfile.objects.get(auth_user_id=user.data["id"]).serializable_value('id')
        if request.data["user_profile_id"] is not None and request.data["user_profile_id"] != '':
            user_profile = request.data["user_profile_id"]
        data = {
            "date": request.data["date"],
            "time_start": request.data["time_start"],
            "time_end": request.data["time_end"],
            "position": request.data["position"],
            "objects_id": request.data["objects_id"],
            "user_profile_id": user_profile,
            "comment": request.data["comment"]
        }
        serializer = TimeReportPostSerializer(data=data)
        # return Response({"data": data}, status=201)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response({"data": data}, status=400)

    def put(self, request):
        saved = get_object_or_404(TimeReport.objects.all(), id=request.data["id"])
        serializer = TimeReportPostSerializer(saved, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request):
        saved = get_object_or_404(TimeReport.objects.all(), id=request.data["id"])
        saved.delete()
        return Response(status=204)


class TimeReportPositionsView(APIView):
    """Профили работ из часовых отчетов"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        positions = TimeReport.objects.all().values_list("position", flat=True).distinct("position")
        return Response({"positions": positions}, status=200)


class UserSettingsView(APIView):
    """Настройки пользователя"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = UserSerializer(request.user)
        user_profile = UserProfile.objects.get(auth_user_id=user.data["id"])
        try:
            serializer = UserSettingsSerializer(user_profile.usersettings)
            return Response({"data": serializer.data}, status=200)
        except UserSettings.DoesNotExist:
            return Response({"data": {
                "theme": "light",
                "language": "ru"
            }})

    def post(self, request):
        new_settings = UserSettingsSerializer(data={
            "user_profile": request.data["user_profile"]
        })
        if new_settings.is_valid():
            new_settings.save()
            return Response(status=201)
        else:
            return Response("Некорректные данные", status=400)

    def put(self, request):
        serializer = None
        user = UserSerializer(request.user)
        user_profile = UserProfile.objects.get(auth_user_id=user.data["id"]).serializable_value('id')
        if user_profile not in UserSettings.objects.all().values_list("user_profile", flat=True):
            serializer = UserSettingsSerializer(data={
                "user_profile": user_profile
            })
        else:
            saved = UserSettings.objects.get(user_profile=user_profile)
            serializer = UserSettingsSerializer(saved, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response("Некорректные данные", status=400)


class ToZipView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        newzip = zipfile.ZipFile('media/accounting/' + request.data['name'] + '.zip', 'w')
        path = request.data['path'].split(';')
        for item in path:
            newzip.write('media' + item)
        newzip.close()
        return Response({"name": 'media/accounting/' + request.data['name'] + '.zip'})

# class ImagesView(APIView):
#     """Загрузка изображений из редактора"""
#     permission_classes = [permissions.AllowAny]
#
#     def post(self, request):
#         return Response({"message": "upload"})
