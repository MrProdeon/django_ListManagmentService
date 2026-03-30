from django.utils import timezone

from django.core.exceptions import ValidationError
from django.db import models
import datetime

from django.db.models import CASCADE
from users.models import CustomUser


# Create your models here.
class MessageModel(models.Model):

    subject_line = models.CharField(max_length=255, blank=True, null=True, verbose_name="Тема письма")
    message_text = models.TextField(verbose_name="Текст сообщения")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

class MailingModel(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_time = models.DateTimeField(verbose_name="Дата и время запуска рассылки")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания рассылки")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default="created", verbose_name="Статус")
    message = models.ForeignKey(to=MessageModel, on_delete=CASCADE)
    recipients = models.ManyToManyField(to=CustomUser)

    def clean(self):
        super().clean()

        if self.start_time and self.start_time < timezone.now():
            raise ValidationError({
                'start_time': 'Время запуска рассылки не может быть в прошлом.'
            })
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError({
                'start_time': 'Время окончания рассылки должно быть позже времени запуска.'
            })

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


    def update_status(self):
        now = timezone.now()

        if now < self.start_time:
            new_status = "created"
        elif now > self.end_time:
            new_status = "completed"
        elif self.start_time <= now <= self.end_time:
            new_status = "started"

        if new_status != self.status:
            self.status = new_status
            self.save(update_fields=["status"])

        return self.status

    def __str__(self):
        return f"Рассылка {self.id} - {self.message.subject_line}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

class AttemptToSend(models.Model):
    STATUS_CHOICES = [
        ("succes", "Успешно"),
        ("unsuccess", "Неуспешно")
    ]

    attempt_time = models.DateTimeField(verbose_name="Дата и время попытки")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    server_response = models.TextField
    mailing = models.ForeignKey(to=MailingModel, on_delete=CASCADE)