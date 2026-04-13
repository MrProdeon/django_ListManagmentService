from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView


from users.views import (CreateRecipient, ListRecipient, DeleteRecipient, DetailRecipient, UpdateRecipient,
                         RegisterView, CustomLoginView, VerifyEmailView, ResendVerificationView, ListUsers)

app_name = "users"

urlpatterns = [
    # RECIPIENTS
    path("admin/", admin.site.urls),
    path("create_recipient/", CreateRecipient.as_view(), name="create_recipient"),
    path("", ListRecipient.as_view(), name="list_recipient"),
    path("update_recipient/<int:pk>/", UpdateRecipient.as_view(), name="update_recipient"),
    path("delete_recipient/<int:pk>/", DeleteRecipient.as_view(), name="delete_recipient"),
    path("detail_recipient/<int:pk>/", DetailRecipient.as_view(), name="detail_recipient"),

    # USERS
    path("register/", RegisterView.as_view(), name="register"),
    path("register/complete/<int:user_id>", TemplateView.as_view(template_name="register_complete.html"),
         name="register_complete"),
    path("register/succes_verify/", TemplateView.as_view(template_name="success_verify.html"), name="success_verify"),
    path("verify/<uuid:token>/", VerifyEmailView.as_view(), name='verify_email'),
    path("resend/<int:user_id>", ResendVerificationView.as_view(), name="resend_verification"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("list_users/", ListUsers.as_view(), name="list_users"),
    path("block_user/<int:user_id>", BlockUser.as_view(), name="block_user"),

    path('reset_password/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('users:password_reset_done')),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

]
