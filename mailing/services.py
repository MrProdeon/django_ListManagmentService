import os

from django.shortcuts import get_object_or_404, redirect
from pyexpat.errors import messages
from django.core.mail import send_mail

from mailing.models import MailingModel
from django.utils import timezone


def start_mailing(request, pk):
    mailing = get_object_or_404(MailingModel,pk)
    now = timezone.now()

    if now < mailing.start_time:
        messages.warning(request, f"Рассылку можно начать только в {mailing.start_time}")
        return redirect('mailing:detail_mailing', pk=pk)

    elif now > mailing.end_time:
        messages.error(request, "Время рассылки истекло")
        return redirect('mailing:detail_mailing', pk=pk)

    elif mailing.start_time <= now <= mailing.end_time:
        messages.succes("Рассылка запущена")

        subject = mailing_object.message.subject_line
        message = mailing_object.message.message_text
        recipient_list = [recipient.email for recepient in mailing_object.recipients]

        for recipient in recipient_list:
            try:
                send = send_mail(subject, message,
                             os.getenv("DEFAULT_FROM_EMAIL"), [recipient],
                             fail_silently=False)
                # Запись в бд об успехе
            except Exception as e:
                pass # Запись в бд об ошибке


    return redirect('mailing:detail_mailing', pk=pk)
