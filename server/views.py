from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
import datetime

from server.serializers import *


class GroupsView(APIView):
    """Группы"""
    permission_classes = [permissions.AllowAny
                          ]

    def get(self, request):
        groups = Group.objects.all()
        serializer = GropSerializer(groups, many=True)
        return Response({"data": serializer.data})
