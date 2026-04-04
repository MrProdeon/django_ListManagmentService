from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from users.models import CustomUser, EmailVerifiedToken
from users.forms import UserForm, CustomUserCreationForm, CustomAuthenticationForm
from django.views import View
from users.services import send_verification_email
from django.contrib import messages

# Create your views here.

class CreateUser(CreateView):
    model = CustomUser
    form_class = UserForm
    template_name = "create_or_update_user.html"
    success_url = reverse_lazy("users:list_user")

class UpdateUser(UpdateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'create_or_update_user.html'
    success_url = reverse_lazy('users:list_user')

class ListUser(ListView):
    model = CustomUser
    template_name = "list_user.html"
    context_object_name = "users"

class DeleteUser(DeleteView):
    model = CustomUser
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("users:list_user")
    context_object_name = "user"

class DetailUser(DetailView):
    model = CustomUser
    template_name = "detail_user.html"
    context_object_name = "user"

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "register.html"
    def get_success_url(self):
        return reverse_lazy('users:register_complete', kwargs={'user_id': self.object.id})

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

            messages.success(request, 'Email успешно подтвержден! Теперь вы можете войти.')
            return redirect('users:success_verify')
        else:
            messages.error(request, 'Ссылка подтверждения истекла. Запросите новую.')
            return redirect('users:resend_verification', user_id=token_obj.user.id)

class ResendVerificationView(View):
    def get(self,request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)

        EmailVerifiedToken.objects.filter(user=user).delete()

        send_verification_email(user)

        messages.success(request, 'Новое письмо с подтверждением отправлено!')
        return redirect('users:login')