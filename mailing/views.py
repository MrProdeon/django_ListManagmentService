from itertools import count

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView, TemplateView
from mailing.models import MessageModel, MailingModel, AttemptToSend
from mailing.forms import MessageCreateForm, MailingCreateForm
from django.views import View
from django.utils import timezone
from users.models import CustomUser
from django.db.models import Count
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.db.models import Q


# Create your views here.
class MessageCreateView(LoginRequiredMixin, CreateView):
    model = MessageModel
    template_name = "create_message.html"
    form_class = MessageCreateForm
    success_url = reverse_lazy("mailing:list_message")
    context_object_name = "message"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = MessageModel
    template_name = "create_message.html"
    form_class = MessageCreateForm
    success_url = reverse_lazy("mailing:list_message")
    context_object_name = "message"

    def get_queryset(self):
        user = self.request.user
        return MessageModel.objects.filet(owner=user)

class MessageListView(LoginRequiredMixin, ListView):
    model = MessageModel
    template_name = "list_message.html"
    context_object_name = "messages"

    def get_queryset(self):
        user = self.request.user

        if user.has_perm("mailing.can_view_all_messages") or user.is_superuser:
            cache_key = "cache_messages_all"
        else:
            cache_key = f"cache_messages_{user.id}"

        queryset = cache.get("cache_messages")

        if queryset is None:
            if user.has_perm("mailing.can_view_all_messages") or user.is_superuser:
                queryset = MessageModel.objects.all()
            else:
                queryset = MessageModel.objects.filter(owner=user)
            cache.set(cache_key, queryset, 300)

        return queryset


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = MessageModel
    template_name = "detail_message.html"
    context_object_name = "message"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (obj.owner == request.user or
                request.user.has_perm("mailing.can_view_all_messages") or
                request.user.is_superuser):
            raise PermissionDenied("Вы не можете детально просматривать сообщения")
        return super().dispatch(request, *args, **kwargs)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = MessageModel
    template_name = "delete_message.html"
    success_url = reverse_lazy("mailing:list_message")
    context_object_name = "message"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if not (obj.user.owner == request.user or
                request.user.has_perm("mailing.can_disable_message") or
                request.user.is_superuser):
            raise PermissionDenied("Вы не можете удалить сообщение")
        return super().dispatch(request, *args, **kwargs)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = MailingModel
    template_name = "create_mailing.html"
    form_class = MailingCreateForm
    success_url = reverse_lazy("mailing:list_mailing")
    context_object_name = "mailing"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        cache.delete(f"cache_messages_{self.request.user.id}")
        cache.delete("cache_messages_all")
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingModel
    template_name = "create_mailing.html"
    form_class = MailingCreateForm
    context_object_name = "mailing"
    success_url = reverse_lazy("mailing:list_mailing")

    def get_queryset(self):
        user = self.request.user
        cache.delete("cache_messages")
        return MailingModel.objects.filter(owner=user)

    def form_valid(self, form):
        response = super().form_valid(form)


        cache.delete(f"cache_messages_{self.request.user.id}")
        cache.delete("cache_messages_all")

        return response


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = MailingModel
    template_name = "detail_mailing.html"
    context_object_name = "mailing"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (obj.owner == request.user or
                request.user.has_perm("mailing.can_view_all_mailings") or
                request.user.is_superuser):
            raise PermissionDenied("Вы не можете детально просматривать рассылку")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=None)
        obj.update_status()
        return obj


class MailingListView(LoginRequiredMixin, ListView):
    model = MailingModel
    context_object_name = "mailings"
    template_name = "list_mailing.html"

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("mailing.can_view_all_mailings") or user.is_superuser:
            queryset =  MailingModel.objects.all()
        else:
            MailingModel.objects.filter(owner=user)

        for mailing in queryset:
            mailing.update_status()

        return queryset


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingModel
    template_name = "delete_mailing.html"
    success_url = reverse_lazy("mailing:list_mailing")
    context_object_name = "mailing"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (obj.owner == request.user or
                request.user.is_superuser):
            raise PermissionDenied("Вы не можете удалять рассылку")
        return super().dispatch(request, *args, **kwargs)


class MailingDisableView(LoginRequiredMixin, UpdateView):
    model = MailingModel
    fields = ["status"]
    template_name = "disable_mailing.html"
    context_object_name = "mailing"
    success_url = reverse_lazy("mailing:list_mailing")

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.has_perm('mailing.can_disable_mailing') or request.user.is_superuser):
            raise PermissionDenied("Вы не можете отключать рассылку")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.status = "disabled"
        return super().form_valid(form)


class MailingMainView(LoginRequiredMixin, TemplateView):
    template_name = "main_mailing.html"

    def get_context_data(self, **kwargs):
        now = timezone.now()
        context = super().get_context_data(**kwargs)

        cache_key = "main_page_stats"
        stats = cache.get(cache_key)

        if not stats:
            now = timezone.now()
            stats = {
                "mailing_counter": MailingModel.objects.count(),
                "active_mailing_count": MailingModel.objects.filter(
                    start_time__lte=now,
                    end_time__gte=now,
                    status="started"
                ).count(),
                "user_count" : CustomUser.objects.count(),
            }

            cache.set(cache_key, stats, 30)

        context.update(stats)
        return context

        # mailing_counter = MailingModel.objects.count()
        # active_mailing_count = MailingModel.objects.filter(
        #     start_time__lte=now,
        #     end_time__gte=now,
        #     status="started"
        # ).count()
        # user_count = CustomUser.objects.count()
        # context["mailing_counter"] = mailing_counter
        # context["active_mailing_count"] = active_mailing_count
        # context["user_count"] = user_count



class ReportView(LoginRequiredMixin, TemplateView):
    template_name = "report.html"

    def get_context_data(self, **kwargs):
        user = self.request.user

        context = super().get_context_data(**kwargs)

        if self.request.user.has_perm("mailing.can_view_all_mailings") or self.request.user.is_superuser:
            user_mailings = MailingModel.objects.all()
        else:
            user_mailings = MailingModel.objects.filter(owner=user)
        context["user_mailings"] = user_mailings
        context["total_mailings"] = user_mailings.count()
        context["total_recipients"] = sum(mailing.recipients.count() for mailing in user_mailings)

        all_attempts = AttemptToSend.objects.filter(mailing__owner=user)
        context["all_attempts"] = all_attempts.count()
        context["success_attempts"] = all_attempts.filter(status="succes").count()
        context["unsuccess_attemps"] = all_attempts.filter(status="unsucces").count()

        return context


class AttemptToSendListView(LoginRequiredMixin, ListView):
    model = AttemptToSend
    template_name = "attempts.html"
    context_object_name = "attempts"
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        mailing_id = self.kwargs.get('pk')


        queryset = AttemptToSend.objects.select_related('mailing', 'mailing__message', 'mailing__owner')


        if mailing_id:
            queryset = queryset.filter(mailing_id=mailing_id)


        if user.is_superuser:

            return queryset

        if user.has_perm('mailing.can_view_all_mailings'):

            return queryset


        return queryset.filter(mailing__owner=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_id = self.kwargs.get('pk')

        if mailing_id:
            from .models import MailingModel
            mailing = MailingModel.objects.get(pk=mailing_id)
            context['mailing'] = mailing

        return context
