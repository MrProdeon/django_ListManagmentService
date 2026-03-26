from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    username = None

    full_name = models.CharField(150, verbose_name="Ф.И.О.")
    phone_number = models.CharField(15, verbose_name="Номер телефона")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    avatar = models.ImageField(blank=True, null=True, verbose_name="Аватар")
    country = models.CharField(50, verbose_name="Страна")

    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

