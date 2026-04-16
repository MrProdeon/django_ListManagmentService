from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailing.models import MailingModel, MessageModel
from users.models import Recipient, CustomUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        manager_group, created = Group.objects.get_or_create(name="Менеджеры")

        if created:
            print("Группа создана")
        else:
            print("Группа уже существует")

        mailing_ct = ContentType.objects.get_for_model(MailingModel)
        message_ct = ContentType.objects.get_for_model(MessageModel)
        client_ct = ContentType.objects.get_for_model(Recipient)
        user_ct = ContentType.objects.get_for_model(CustomUser)

        permissions = [
            # Рассылки
            ("can_view_all_mailings", "Может просматривать все рассылки"),
            ("can_disable_mailing", "Может отключать рассылки"),
            # Сообщения
            ("can_view_all_messages", "Может просматривать все сообщения"),
            ("can_disable_message", "Может отключать сообщения"),
            # Получатели
            ("can_view_all_recipients", "Может просматривать всех получателей"),
            ("can_block_recipients", "Может блокировать получателей"),
            # Пользователи
            ("can_block_users", "Может блокировать пользователей"),
        ]

        for codename, name in permissions:
            try:
                if "mailing" in codename:
                    permission = Permission.objects.get(
                        codename=codename, content_type=mailing_ct
                    )
                elif "message" in codename:
                    permission = Permission.objects.get(
                        codename=codename, content_type=message_ct
                    )
                elif "recipient" in codename:
                    permission = Permission.objects.get(
                        codename=codename, content_type=client_ct
                    )
                elif "user" in codename:
                    permission = Permission.objects.get(
                        codename=codename, content_type=user_ct
                    )
                else:
                    continue

                manager_group.permissions.add(permission)
                print(f"Добавлено право: {name}")
            except Permission.DoesNotExist:
                print(f"Право {codename} не найдено")

        print("Группа менеджеров успешно настроена")
