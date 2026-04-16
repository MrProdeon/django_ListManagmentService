from django.contrib import admin
from users.models import Recipient, CustomUser

# Register your models here.
@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'full_name',
        'phone_number',
        'country',
        'is_email_verified',
        'created_at',
        'updated_at',
        'comment',
        'avatar',
    )
    list_filter = ("created_at", "owner")
    search_fields = ("email", "owner", "full_name")

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
    "id",
    "full_name",
    "phone_number",
    "comment",
    "avatar",
    "country",
    "created_at",
    "updated_at",
    "email",
    "is_email_verified",
)
    list_filter = ("created_at", "is_email_verified")
    search_fields = ("email", "full_name")