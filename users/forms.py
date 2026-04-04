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