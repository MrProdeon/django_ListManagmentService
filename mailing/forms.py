from django.forms import ModelForm
from mailing.models import MessageModel


class MessageCreateForm(ModelForm):

    class Meta:
        model = MessageModel
        fields = ['subject_line', 'message_text']