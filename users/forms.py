from django.forms import ModelForm
from users.models import CustomUser

class UserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["full_name", "phone_number", "country", "email", "avatar"]