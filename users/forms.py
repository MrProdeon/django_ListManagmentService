from django.forms import ModelForm
from users.models import CustomUser, Recipient
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
)
from django import forms


# RECIPIENTS
class RecipientForm(ModelForm):
    class Meta:
        model = Recipient
        fields = ["full_name", "phone_number", "country", "email", "avatar"]


# USERS
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "full_name", "phone_number", "avatar", "country")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user


class CustomUserUpdatingForm(UserChangeForm):
    password = None

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "full_name", "phone_number", "avatar", "country")


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
        label="Email",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Пароль"}
        ),
        label="Пароль",
    )

    error_messages = {
        "invalid_login": "Неверный email или пароль",
        "inactive": "Аккаунт деактивирован",
    }

    def confirm_login_allowed(self, user):
        """Дополнительная проверка при входе"""
        if not user.is_active:
            raise forms.ValidationError(
                "Email не подтвержден. Проверьте почту или запросите новое письмо.",
                code="inactive",
            )
