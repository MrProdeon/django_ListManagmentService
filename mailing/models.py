from django.db import models

# Create your models here.
class MessageModel(models.Model):

    subject_line = models.CharField(max_length=255, blank=True, null=True, verbose_name="Тема письма")
    message_text = models.TextField(verbose_name="Текст сообщения")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"