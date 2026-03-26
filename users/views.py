from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.models import CustomUser


# Create your views here.

class CreateUser(CreateView):
    model = CustomUser
    fields = ["full_name", "phone_number", "country", "email", "avatar"]
    template_name = "create_or_update_user.html"
    success_url = reverse_lazy("list_users")
