from django.shortcuts import render
from django.views.generic import CreateView, ListView
from mailing.models import MessageModel
from mailing.forms import MessageCreateForm


# Create your views here.
class MessageCreateView(CreateView):
    model = MessageModel
    template_name = "create_message.html"
    form_class = MessageCreateForm
    success_url = 0

class MessageListView(ListView):
    model = MessageModel
    template_name = "list_message.html"
    context_object_name = "messages"
