from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView
from users.models import CustomUser
from users.forms import UserForm

# Create your views here.

class CreateUser(CreateView):
    model = CustomUser
    form_class = UserForm
    template_name = "create_or_update_user.html"
    success_url = reverse_lazy("users:list_users")

class ListUser(ListView):
    model = CustomUser
    template_name = "list_user.html"
    context_object_name = "users"

class DeleteUser(DeleteView):
    model = CustomUser
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("users:list_user")
    context_object_name = "user"