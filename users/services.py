from django.core.mail import send_mail
from config import settings
from django.urls import reverse
from users.models import EmailVerifiedToken

def send_verification_email(user):
    token, created = EmailVerifiedToken.objects.get_or_create(user=user)

    verification_url = reverse("users:verify_email", kwargs={"token" : token.token})
    full_url = f"{settings.SITE_URL}{verification_url}"

    subject = "Подтвердите вашу электронную почту"
    message = f"""
Здравствуйте, {user.full_name}

Для подтверждения вашей электронной почты, пожалуйста, перейдите по ссылке:
{full_url}

Ссылка действительна 24 часа.
"""
    send_mail(subject=subject,message=message, from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[user.email], fail_silently=False)