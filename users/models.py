import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import CASCADE
from django.utils import timezone


# Create your models here.
class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    username = None

    full_name = models.CharField(max_length=150, verbose_name="Ф.И.О.")
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    avatar = models.ImageField(blank=True, null=True, verbose_name="Аватар")
    country = models.CharField(max_length=50, verbose_name="Страна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")


    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    is_email_verified = models.BooleanField(default=False, verbose_name="Подтвержден ли email")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("can_view_all_recipients", "Может просматривать всех получателей"),
            ("can_block_recipients", "Может блокировать получателей"),
        ]


class Recipient(models.Model):
    first_name = None
    last_name = None
    username = None

    full_name = models.CharField(max_length=150, verbose_name="Ф.И.О.")
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    avatar = models.ImageField(blank=True, null=True, verbose_name="Аватар")
    country = models.CharField(max_length=50, verbose_name="Страна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    owner = models.ForeignKey(to=CustomUser, on_delete=models.SET_NULL, verbose_name="Владелец рассылки", null=True)


    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    is_email_verified = models.BooleanField(default=False, verbose_name="Подтвержден ли email")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"

class EmailVerifiedToken(models.Model):
    user = models.OneToOneField(to=CustomUser, on_delete=CASCADE, verbose_name="Пользователь")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def is_valid():
        expire_time = timezone.now() + timezone.timedelta(hours=24)
        return timezone.now() <= expire_time

    def __str__(self):
        return f"Токен для {self.user.email}"