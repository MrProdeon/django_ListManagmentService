from django.contrib import admin
from mailing.models import MessageModel, MailingModel, AttemptToSend


# Register your models here.
@admin.register(MessageModel)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject_line", "message_text", "created_at", "updated_at", "owner")
    list_filter = ("created_at", "owner")
    search_fields = ("subect_line", "owner")


@admin.register(MailingModel)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "message",
        "status",
        "owner",
        "start_time",
        "end_time",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "owner", "created_at", "start_time")
    search_fields = ("message__subject_line", "owner__email", "status")


@admin.register(AttemptToSend)
class AttemptToSendAdmin(admin.ModelAdmin):
    list_display = ("id", "attempt_time", "status", "server_response", "mailing")
