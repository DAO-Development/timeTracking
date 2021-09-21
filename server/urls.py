# Urls for server app

from django.urls import path
from server.views import *

urlpatterns = [
    # path('users', UsersView.as_view()),
    # path('users/<int:idclient>', UsersView.as_view()),
    path('group', GroupView.as_view()),
    path('groups', GroupsView.as_view()),
    path('news', NewsView.as_view()),
    path('news/<int:id>', NewsView.as_view()),
    path('objects', ObjectsView.as_view()),
    path('objects/<int:id>', ObjectsView.as_view()),
    # path('user/objects', UserObjectView.as_view()),
    path('objects/employees/<int:objects_id>', ObjectUserView.as_view()),
]
