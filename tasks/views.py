from typing import Any
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from .models import *


class RegistrationView(UserPassesTestMixin, FormView):

    def test_func(self) -> bool | None:
        return not self.request.user.is_authenticated

    template_name = "tasks/register.html"
    form_class = UserCreationForm
    success_url = "login"

    def form_valid(self, form):

        user = form.save()
        login(self.request, user)

        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = "tasks/login.html"
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy("index")

@method_decorator(login_required, name="dispatch")
class TasksListView(ListView):
    model = Task
    template_name = "tasks/index.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)

        search_input = self.request.GET.get("search_input") or ""
        if search_input:
            context["tasks"] = context["tasks"].filter(title__contains=search_input)

        context["search_input"] = search_input

        return context

@method_decorator(login_required, name="dispatch")
class TaskCreateView(CreateView):
    model = Task
    fields = ["title", "description", "completed"]
    template_name = "tasks/task_create.html"
    success_url = reverse_lazy("index")\
    
    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)
    
@method_decorator(login_required, name="dispatch")
class TaskUpdateView(UserPassesTestMixin, UpdateView):

    def test_func(self) -> bool | None:
        
        pk =self.get_object().pk

        return Task.objects.get(pk=pk).user == self.request.user

    model = Task
    fields = ["title", "description", "completed"]
    template_name = "tasks/task_update.html"
    success_url = reverse_lazy("index")

@method_decorator(login_required, name="dispatch")
class TaskDeleteView(UserPassesTestMixin, DeleteView):

    def test_func(self) -> bool | None:
        
        pk =self.get_object().pk

        return Task.objects.get(pk=pk).user == self.request.user

    model = Task
    template_name = "tasks/task_detele.html"
    success_url = reverse_lazy("index")

    
    