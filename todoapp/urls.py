from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('',views.home , name='home-page'),
    path("register/",views.register, name ='register'),
    path("login/",views.login, name = "login.html"),
    path("delete-task/<str:name>",views.DeleteTask , name="delete"),
    path("update/<str:name>",views.Update , name = "update"),
]
