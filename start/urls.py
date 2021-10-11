# Urls for server app

from django.urls import path
import views

urlpatterns = [
    path('', views.start),
]
