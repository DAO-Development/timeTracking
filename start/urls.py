# Urls for server app

from django.urls import path
from start.views import start

urlpatterns = [
    path('', start),
]
