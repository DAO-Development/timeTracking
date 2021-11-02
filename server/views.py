from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
import datetime

from server.serializers import *


class UserView(APIView):
    """Пользователи"""
    permission_classes = [permissions.IsAuthenticated]

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
            "is_staff": request.data["is_staff"],
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


class ProfilesView(APIView):
    """Получение списка работников, профили"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_profile = UserProfile.objects.all().order_by('lastname').order_by('name')
        serializer = UserProfileSerializer(user_profile, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        serializer = UserProfilePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=201)
        else:
            return Response(status=400)

    def put(self, request, id=None):
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
                return Response(status=400)
        saved_profile = get_object_or_404(UserProfile.objects.all(), id=request.data['id'])
        serializer = UserProfileSerializer(saved_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)


class UserDocumentsView(APIView):
    """Документы пользователей"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, ):
        # return Response({"data": request.GET['id']})
        profile = get_object_or_404(UserProfile.objects.all(), pk=request.GET['id'])
        profile_serializer = UserProfileSerializer(profile)
        documents = UserDocuments.objects.all().filter(user_profile_id=request.GET['id'])
        serializer = UserDocumentsSerializer(documents, many=True)
        return Response({"profile": profile_serializer.data, "documents": serializer.data}, status=200)

    def put(self, request):
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
            return Response(status=400)

    def delete(self, request):
        document = get_object_or_404(UserDocuments.objects.all(), id=request.data["id"])
        document.delete()
        return Response(status=204)


class GroupView(APIView):
    """Группа пользователя"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = UserSerializer(request.user)
        group = Group.objects.filter(user=user.data["id"])
        serializer = GroupSerializer(group, many=True)
        return Response({"data": serializer.data})


class GroupsView(APIView):
    """Группы"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response({"data": serializer.data})


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
        serializer = NewsPostSerializer(data={
            "title": request.data["title"],
            "text": request.data["text"],
            "photo_path": name
        })
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def put(self, request):
        saved_news = get_object_or_404(News.objects.all(), id=request.data["id"])
        name = ''
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

    def get(self, request):
        user = UserSerializer(request.user)
        objects = Objects.objects.all()
        if not user.data["is_staff"]:
            user_profile = UserProfileSerializer(UserProfile.objects.get(auth_user_id=user.data["id"]))
            objects_user = ObjectUser.objects.filter(user_profile_id=user_profile.data["id"]).values_list('objects_id',
                                                                                                          flat=True)
            objects = Objects.objects.filter(pk__in=objects_user)
        serializer = ObjectsSerializer(objects, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        serializer = ObjectsPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def put(self, request):
        saved_object = get_object_or_404(Objects.objects.all(), id=request.data["id"])
        data = request.data
        serializer = ObjectsSerializer(saved_object, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request):
        object = get_object_or_404(Objects.objects.all(), id=request.data["id"])
        object.delete()
        return Response(status=204)


class ObjectUserView(APIView):
    """Рабочие на объектах"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, objects_id=None):
        if objects_id is not None:
            workers = ObjectUser.objects.all().filter(objects_id=objects_id)
            serializer = ObjectUserSerializer(workers, many=True)
        else:
            busy = ObjectUser.objects.all().filter(end_date__gt=datetime.date.today()).values_list('user_profile_id',
                                                                                                   flat=True)
            workers = UserProfile.objects.all().exclude(id__in=busy)
            serializer = UserProfileSerializer(workers, many=True)
        return Response({"data": serializer.data})

    def put(self, request):
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
            return Response(status=400)

    def delete(self, request):
        object_user = get_object_or_404(ObjectUser.objects.all(), id=request.data['id'])
        object_user.delete()
        return Response(status=204)


class ObjectPhotoView(APIView):
    """Фото объектов"""
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
            serializer = ObjectPhotoPostSerializer(data={
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
        clients = Client.objects.all()
        if id is not None:
            clients = clients.filter(pk=id)
        else:
            clients = clients.order_by('name')
        serializer = ClientSerializer(clients, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        serializer = ClientPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def put(self, request):
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
            return Response(status=400)

    def delete(self, request):
        saved_client = get_object_or_404(Client.objects.all(), id=request.data["id"])
        saved_client.delete()
        return Response(status=204)


class ClientEmployeesView(APIView):
    """Сотрудники фирм-клиентов"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, client_id=None):
        employees = ClientEmployees.objects.all()
        if client_id is not None:
            employees = employees.filter(client=client_id)
        serializer = ClientEmployeesSerializer(employees, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        serializer = ClientEmployeesPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def put(self, request):
        saved_employee = get_object_or_404(ClientEmployees.objects.all(), id=request.data["id"])
        serializer = ClientSerializer(saved_employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request):
        saved_employee = get_object_or_404(ClientEmployees.objects.all(), id=request.data["id"])
        saved_employee.delete()
        return Response(status=204)


class ImagesView(APIView):
    """Загрузка изображений из редактора"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        return Response({"message": "upload"})
