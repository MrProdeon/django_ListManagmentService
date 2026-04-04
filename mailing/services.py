import os

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail

from mailing.models import MailingModel, AttemptToSend
from django.utils import timezone


def start_mailing(request, pk):
    mailing = get_object_or_404(MailingModel,pk=pk)
    now = timezone.now()

    if now < mailing.start_time:
        messages.warning(request, f"Рассылку можно начать только в {mailing.start_time}")
        return redirect('mailing:detail_mailing', pk=pk)

    elif now > mailing.end_time:
        messages.error(request, "Время рассылки истекло")
        return redirect('mailing:detail_mailing', pk=pk)

    elif mailing.start_time <= now <= mailing.end_time:
        messages.success(request, "Рассылка запущена")

        subject = mailing.message.subject_line
        message = mailing.message.message_text
        recipient_list = [recipient.email for recipient in mailing.recipients.all()]

        for recipient in recipient_list:
            try:
                send_mail(subject, message, os.getenv("DEFAULT_FROM_EMAIL"), [recipient],
                             fail_silently=False)
                attempt = AttemptToSend.objects.create(attempt_time=now, status="succes",
                                                       server_response="Письмо отправлено", mailing=mailing)
                attempt.save()

            except Exception as e:
                attempt = AttemptToSend.objects.create(attempt_time=now, status="unsucces",
                                                       server_response=f"Ошибка: {e}", mailing=mailing)
                attempt.save()


    return redirect('mailing:detail_mailing', pk=pk)
