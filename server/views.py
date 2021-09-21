from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
import datetime

from server.serializers import *


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

    def put(self, request, id):
        saved_news = get_object_or_404(News.objects.all(), id=id)
        data = request.data
        serializer = NewsSerializer(saved_news, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request, id):
        news = get_object_or_404(News.objects.all(), id=id)
        news.delete()
        return Response(status=204)


class ObjectsView(APIView):
    """Объекты"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        objects = Objects.objects.all()
        serializer = ObjectsSerializer(objects, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        serializer = ObjectsPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)


def put(self, request, id):
    saved_object = get_object_or_404(Objects.objects.all(), id=id)
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
