from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    DeleteView,
    DetailView,
    UpdateView,
    TemplateView,
)
from prompt_toolkit.validation import ValidationError

from users.models import CustomUser, EmailVerifiedToken, Recipient
from users.forms import (
    RecipientForm,
    CustomUserCreationForm,
    CustomAuthenticationForm,
    CustomUserUpdatingForm,
)
from django.views import View
from users.services import send_verification_email
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache


# RECIPIENTS
class CreateRecipient(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "create_or_update_recipient.html"
    success_url = reverse_lazy("users:list_recipient")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        cache.delete(f"recipient_list_{self.request.user.id}")
        return response


class UpdateRecipient(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "create_or_update_recipient.html"
    success_url = reverse_lazy("users:list_recipient")

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete(f"recipient_list_{self.request.user.id}")
        return response

    def get_queryset(self):
        user = self.request.user

        return Recipient.objects.filter(owner=user)


class ListRecipient(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "list_recipient.html"
    context_object_name = "users"

    def get_queryset(self):
        user = self.request.user
        cache_key = f"recipient_list_{user.id}"

        queryset = cache.get(cache_key)

        if queryset is None:
            if user.has_perm("users.can_view_all_recipients") or user.is_superuser:
                queryset = Recipient.objects.all()
            else:
                queryset = Recipient.objects.filter(owner=user)

            cache.set(cache_key, queryset, 300)
        return queryset


@method_decorator(cache_page(60 * 5), name="dispatch")
class ListUsers(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "list_users.html"
    context_object_name = "users"

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("users.can_view_all_recipients") or user.is_superuser:
            return CustomUser.objects.all()
        raise PermissionDenied("Вы не можете просматривать пользователей")


class DeleteRecipient(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("users:list_recipient")
    context_object_name = "user"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (
            obj.owner == request.user
            or request.user.is_superuser
            or request.user.has_perm("users.can_block_recipients")
        ):
            raise PermissionDenied("Вы не можете удалять пользователя")
        return super().dispatch(request, *args, **kwargs)


class DetailRecipient(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = "detail_recipient.html"
    context_object_name = "user"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (
            obj.owner == request.user
            or request.user.has_perm("users.can_view_all_recipients")
            or request.user.is_superuser
        ):
            raise PermissionDenied("Вы не можете детально просматривать получателей")
        return super().dispatch(request, *args, **kwargs)


# USERS


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "register.html"

    def get_success_url(self):
        return reverse_lazy(
            "users:register_complete", kwargs={"user_id": self.object.id}
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        send_verification_email(self.object)
        return response


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = "login.html"


class VerifyEmailView(View):

    def get(self, request, token):
        token_obj = get_object_or_404(EmailVerifiedToken, token=token)

        if token_obj.is_valid():
            user = token_obj.user
            user.is_active = True
            user.is_email_verified = True
            user.save()

            token_obj.delete()

            messages.success(
                request, "Email успешно подтвержден! Теперь вы можете войти."
            )
            return redirect("users:success_verify")
        else:
            messages.error(request, "Ссылка подтверждения истекла. Запросите новую.")
            return redirect("users:resend_verification", user_id=token_obj.user.id)


class CreateUser(LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "create_or_update_user.html"
    success_url = reverse_lazy("users:list_users")


class UpdateUser(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdatingForm
    template_name = "create_or_update_user.html"
    success_url = reverse_lazy("users:list_users")


class DetailUser(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "detail_user.html"
    context_object_name = "user"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (
            request.user.has_perm("users.can_view_all_recipients")
            or request.user.is_superuser
        ):
            raise PermissionDenied("Вы не можете детально просматривать пользователей")
        return super().dispatch(request, *args, **kwargs)


class DeleteUser(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "delete_user.html"
    success_url = reverse_lazy("users:list_users")
    context_object_name = "user"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (
            request.user.is_superuser
            or request.user.has_perm("users.can_block_recipients")
        ):
            raise PermissionDenied("Вы не можете удалять пользователя")
        return super().dispatch(request, *args, **kwargs)


class ResendVerificationView(View):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)

        EmailVerifiedToken.objects.filter(user=user).delete()

        send_verification_email(user)

        messages.success(request, "Новое письмо с подтверждением отправлено!")
        return redirect("users:login")


class BlockUser(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ["is_active"]
    template_name = "block_user.html"
    success_url = reverse_lazy("users:list_users")
    context_object_name = "user"

    def dispatch(self, request, *args, **kwargs):
        if not (
            request.user.has_perm("users.can_block_users") or request.user.is_superuser
        ):
            raise PermissionDenied("Вы не можете блокировать пользователей")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = not user.is_active
        user.save()
        return super().form_valid(form)
