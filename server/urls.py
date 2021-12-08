# Urls for server app

from django.urls import path
from server.views import *

urlpatterns = [
    path('statistics', MainView.as_view()),
    path('user', UserView.as_view()),
    path('user-groups', UserGroupsView.as_view()),
    path('profiles', ProfilesView.as_view()),
    path('profiles/positions', PositionProfileView.as_view()),
    path('profiles/<int:id>', ProfilesView.as_view()),
    path('group', GroupView.as_view()),
    path('groups', GroupsView.as_view()),
    path('groups-functions', GroupFunctionsView.as_view()),
    path('news', NewsView.as_view()),
    path('news/<int:id>', NewsView.as_view()),
    path('objects', ObjectsView.as_view()),
    path('objects/employees', ObjectUserView.as_view()),
    path('objects/employees/<int:objects_id>', ObjectUserView.as_view()),
    path('objects/comments', ObjectCommentsView.as_view()),
    path('objects/comments/<int:id>', ObjectCommentsView.as_view()),
    path('objects/photos/<int:objects_id>', ObjectPhotoView.as_view()),
    path('clients', ClientView.as_view()),
    path('clients/branches', ClientBranchesView.as_view()),
    path('clients/<int:id>', ClientView.as_view()),
    path('clients-employees', ClientEmployeesView.as_view()),
    path('clients/employees/<int:idclient>', ClientEmployeesView.as_view()),
    path('clients-employees/<int:id>', ClientEmployeesView.as_view()),
    path('clients-employees/positions', PositionClientView.as_view()),
    path('documents/worker', UserDocumentsView.as_view()),
    path('notes', NotesView.as_view()),
    path('images/upload', ImagesView.as_view()),
]
