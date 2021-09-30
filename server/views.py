from django.shortcuts import render

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
        saved_user = get_object_or_404(User.objects.all(), email=request.data['email'])
        serializer = UserSerializer(saved_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
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
        user_profile = UserProfile.objects.all()
        serializer = UserProfileSerializer(user_profile, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        serializer = UserProfilePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=201)
        else:
            return Response(status=400)

    def put(self, request):
        saved_profile = get_object_or_404(UserProfile.objects.all(), id=request.data['id'])
        serializer = UserProfileSerializer(saved_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)


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
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        user = UserSerializer(request.user)
        user_profile = UserProfileSerializer(get_object_or_404(UserProfile.objects.all(), auth_user_id=user.data["id"]))
        serializer = NewsPostSerializer(data={
            "title": request.data["title"],
            "text": request.data["text"],
            "author": user_profile.data["id"]
        })
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def put(self, request):
        saved_news = get_object_or_404(News.objects.all(), id=request.data["id"])
        data = request.data
        serializer = NewsSerializer(saved_news, data=data, partial=True)
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

    def delete(self, request, id):
        object = get_object_or_404(Objects.objects.all(), id=id)
        object.delete()
        return Response(status=204)


class ObjectUserView(APIView):
    """Рабочие на объектах"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, objects_id):
        objects = Objects.objects.all().filter(objects_id=objects_id)
        serializer = ObjectsSerializer(objects, many=True)
        return Response({"data": serializer.data})

    def put(self, request):
        if request.data['id'] != '':
            saved_object = ObjectUser.objects.get(pk=request.data['id'])
            serializer = ObjectUserSerializer(saved_object, data=request.data, partial=True)
        else:
            serializer = ObjectUserPostSerializer(data={
                "user_profile_id": request.data['user_profile_id'],
                "objects_id": request.data['objects_id'],
            })
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request):
        object_user = get_object_or_404(Objects.objects.all(), id=request.data['id'])
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
        object_photo = get_object_or_404(Objects.objects.all(), id=id)
        object_photo.delete()
        return Response(status=204)


class ClientView(APIView):
    """Клиенты"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response({"data": serializer.data})

    # def put(self, request):
    #     if request.data['id'] != '':
    #         saved_object = ObjectPhoto.objects.get(pk=request.data['id'])
    #         serializer = ObjectPhoto(saved_object, data=request.data, partial=True)
    #     else:
    #         serializer = ObjectPhotoPostSerializer(data={
    #             "photo_path": request.data['photo_path'],
    #             "objects_id": request.data['objects_id'],
    #         })
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(status=201)
    #     else:
    #         return Response(status=400)
    #
    # def delete(self, request, id):
    #     object_photo = get_object_or_404(Objects.objects.all(), id=id)
    #     object_photo.delete()
    #     return Response(status=204)
