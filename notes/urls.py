from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signUpView, name="signUp"),
    path("login/", views.logInView, name="logIn"),
    path("logout/", views.logOut, name="logOut"),
    path("notes/",views.notesView, name="notes"),
    path("add/", views.addView, name="add")
]