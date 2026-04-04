from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from users.views import (CreateUser, ListUser, DeleteUser, DetailUser, UpdateUser,
                         RegisterView, CustomLoginView, VerifyEmailView, ResendVerificationView)

app_name = "users"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("create_user/", CreateUser.as_view(), name="create_user"),
    path("", ListUser.as_view(), name="list_user"),
    path("update_user/<int:pk>/", UpdateUser.as_view(), name="update_user"),
    path("delete_user/<int:pk>/", DeleteUser.as_view(), name="delete_user"),
    path("detail_user/<int:pk>/", DetailUser.as_view(), name="detail_user"),
    path("register/", RegisterView.as_view(), name="register"),
    path("register/complete/<int:user_id>", TemplateView.as_view(template_name="register_complete.html"), name="register_complete"),
    path("register/succes_verify/", TemplateView.as_view(template_name="success_verify.html"), name="success_verify"),
    path("verify/<uuid:token>/", VerifyEmailView.as_view(), name='verify_email'),
    path("resend/<int:user_id>", ResendVerificationView.as_view(), name="resend_verification"),
    path("login/", CustomLoginView.as_view(), name="login")
]
