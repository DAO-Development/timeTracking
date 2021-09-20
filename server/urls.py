# Urls for server app

from django.urls import path
from server.views import *

urlpatterns = [
    # path('users', UsersView.as_view()),
    path('group', GroupView.as_view()),
    path('groups', GroupsView.as_view()),
    path('news', NewsView.as_view()),
    path('news/<int:id>', NewsView.as_view()),
    # path('users/<int:idclient>', UsersView.as_view()),
]
