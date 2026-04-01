from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView, TemplateView
from mailing.models import MessageModel, MailingModel
from mailing.forms import MessageCreateForm, MailingCreateForm
from django.views import View
from django.utils import timezone
from users.models import CustomUser


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

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=None)
        obj.update_status()
        return obj

class MailingListView(ListView):
    model = MailingModel
    context_object_name = "mailings"
    template_name = "list_mailing.html"

class MailingDeleteView(DeleteView):
    model = MailingModel
    template_name = "delete_mailing.html"
    success_url = reverse_lazy("mailing:list_mailing")
    context_object_name = "mailing"

class MailingMainView(TemplateView):
    template_name = "main_mailing.html"

    def get_context_data(self, **kwargs):
        now = timezone.now()
        context = super().get_context_data(**kwargs)

        mailing_counter = MailingModel.objects.count()
        active_mailing_count = MailingModel.objects.filter(
            start_time__lte=now,
            end_time__gte=now,
            status="started"
        ).count()
        user_count = CustomUser.objects.count()
        context["mailing_counter"] = mailing_counter
        context["active_mailing_count"] = active_mailing_count
        context["user_count"] = user_count

        return context