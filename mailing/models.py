from django.utils import timezone

from django.core.exceptions import ValidationError
from django.db import models
import datetime

from django.db.models import CASCADE, SET_NULL
from users.models import CustomUser, Recipient


# Create your models here.
class MessageModel(models.Model):

    subject_line = models.CharField(max_length=255, blank=True, null=True, verbose_name="Тема письма")
    message_text = models.TextField(verbose_name="Текст сообщения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    owner = models.ForeignKey(to=CustomUser, on_delete=models.SET_NULL, null=True, verbose_name="Владелец")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.subject_line


    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        permissions = [
            ("can_view_all_messages", "Может просматривать все сообщения"),
            ("can_disable_message", "Может отключать сообщения"),
        ]
class MailingModel(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
        ('disables', "Отключена")
    ]

    start_time = models.DateTimeField(verbose_name="Дата и время запуска рассылки")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания рассылки")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default="created", verbose_name="Статус")
    message = models.ForeignKey(to=MessageModel, on_delete=CASCADE)
    recipients = models.ManyToManyField(to=Recipient)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    owner = models.ForeignKey(to=CustomUser, on_delete=SET_NULL, verbose_name="Владелец рассылки", null=True)

    # def clean(self):
    #     super().clean()
    #
    #     if self.start_time and self.start_time < timezone.now():
    #         messages.error(request, "Время рассылки истекло")
    #     if self.start_time and self.end_time and self.start_time >= self.end_time:
    #         raise ValidationError({
    #             'start_time': 'Время окончания рассылки должно быть позже времени запуска.'
    #         })
    #
    # def save(self, *args, **kwargs):
    #     self.clean()
    #     super().save(*args, **kwargs)


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
        permissions = [
            ("can_view_all_mailings", "Может просматривать все рассылки"),
            ("can_disable_mailing", "Может отключать рассылки")
        ]

class AttemptToSend(models.Model):
    STATUS_CHOICES = [
        ("succes", "Успешно"),
        ("unsuccess", "Неуспешно")
    ]

    attempt_time = models.DateTimeField(verbose_name="Дата и время попытки")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    server_response = models.TextField()
    mailing = models.ForeignKey(to=MailingModel, on_delete=CASCADE)