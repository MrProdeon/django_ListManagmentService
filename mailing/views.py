from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from mailing.models import MessageModel
from mailing.forms import MessageCreateForm


# Create your views here.
class MessageCreateView(CreateView):
    model = MessageModel
    template_name = "create_message.html"
    form_class = MessageCreateForm
    success_url = reverse_lazy("mailing:list_message")
    context_object_name = "message"

class MessageUpdateView(UpdateView):
    model = MessageModel
    template_name = "create_message.html"
    form_class = MessageCreateForm
    success_url = reverse_lazy("mailing:list_message")
    context_object_name = "message"

class MessageListView(ListView):
    model = MessageModel
    template_name = "list_message.html"
    context_object_name = "messages"

class MessageDetailView
