from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    username = None

    full_name = models.CharField(max_length=150, verbose_name="Ф.И.О.")
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    avatar = models.ImageField(blank=True, null=True, verbose_name="Аватар")
    country = models.CharField(max_length=50, verbose_name="Страна")

    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

