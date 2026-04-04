from django.forms import ModelForm
from users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class UserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["full_name", "phone_number", "country", "email", "avatar"]

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

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        }),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        }),
        label='Пароль'
    )

    error_messages = {
        'invalid_login': 'Неверный email или пароль',
        'inactive': 'Аккаунт деактивирован',
    }

    def confirm_login_allowed(self, user):
        """Дополнительная проверка при входе"""
        if not user.is_active:
            raise forms.ValidationError(
                "Email не подтвержден. Проверьте почту или запросите новое письмо.",
                code='inactive',
            )