from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.models import CustomUser
from users.forms import UserForm

# Create your views here.

class CreateUser(CreateView):
    model = CustomUser
    form_class = UserForm
    template_name = "create_or_update_user.html"
    success_url = reverse_lazy("list_users")
