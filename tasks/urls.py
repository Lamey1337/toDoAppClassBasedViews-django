from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path("register", RegistrationView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="index"), name="logout"),
    path("", TasksListView.as_view(), name="index"),
    path("create/", TaskCreateView.as_view(), name="create"),
    path("delete/<int:pk>", TaskDeleteView.as_view(), name="delete"),
    path("task/<int:pk>", TaskUpdateView.as_view(), name="edit"),
]



