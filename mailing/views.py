from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from mailing.models import MessageModel, MailingModel
from mailing.forms import MessageCreateForm, MailingCreateForm


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

class MessageDetailView(DetailView):
    model = MessageModel
    template_name = "detail_message.html"
    context_object_name = "message"

class MessageDeleteView(DeleteView):
    model = MessageModel
    template_name = "delete_message.html"
    success_url = reverse_lazy("mailing:list_message")
    context_object_name = "message"

class MailingCreateView(CreateView):
    model = MailingModel
    template_name = "create_mailing.html"
    form_class = MailingCreateForm
    success_url = reverse_lazy("mailing:list_mailing")
    context_object_name = "mailing"

class MailingUpdateView(UpdateView):
    model = MailingModel
    template_name = "create_mailing.html"
    form_class = MailingCreateForm
    context_object_name = "mailing"
    success_url = reverse_lazy("mailing:list_mailing")

class MailingDetailView(DetailView):
    model = MailingModel
    template_name = "detail_mailing.html"
    context_object_name = "mailing"

class MailingListView(ListView):
    model = MailingModel
    context_object_name = "mailings"
    template_name = "list_mailing.html"