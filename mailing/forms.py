from django.forms import ModelForm
from mailing.models import MessageModel, MailingModel


class MessageCreateForm(ModelForm):

    class Meta:
        model = MessageModel
        fields = ["subject_line", "message_text"]


class MailingCreateForm(ModelForm):

    class Meta:
        model = MailingModel
        fields = ["start_time", "end_time", "status", "message", "recipients"]
