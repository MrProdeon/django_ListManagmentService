from django.forms import ModelForm
from mailing.models import MessageModel


class MessageCreateForm(ModelForm):
    model = MessageModel