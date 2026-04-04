from django.forms import ModelForm
from users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class UserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["full_name", "phone_number", "country", "email", "avatar"]

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "full_name", "phone_number", "avatar", "country")