from django.contrib import admin
from django.urls import path
from mailing.views import (MessageCreateView, MessageListView, MessageUpdateView,
                           MessageDetailView, MessageDeleteView, MailingCreateView,
                           MailingListView, MailingDetailView, MailingUpdateView,
                           MailingDeleteView, MailingMainView, ReportView)
from mailing.services import start_mailing
app_name = "mailing"

urlpatterns = [
    path("admin/", admin.site.urls),

    #messages
    path("list_message/", MessageListView.as_view(), name="list_message"),
    path("create_message/", MessageCreateView.as_view(), name="create_message"),
    path("update_message/<int:pk>", MessageUpdateView.as_view(), name="update_message"),
    path("detail_message/<int:pk>", MessageDetailView.as_view(), name="detail_message"),
    path("delete_message/<int:pk>", MessageDeleteView.as_view(), name="delete_message"),

    #mailings
    path("", MailingMainView.as_view(), name="mailing_main"),
    path("create_mailing/", MailingCreateView.as_view(), name="create_mailing"),
    path("list_mailing/", MailingListView.as_view(), name="list_mailing"),
    path("detail_mailing/<int:pk>", MailingDetailView.as_view(), name="detail_mailing"),
    path("update_mailing/<int:pk>", MailingUpdateView.as_view(), name="update_mailing"),
    path("delete_mailing/<int:pk>", MailingDeleteView.as_view(), name="delete_mailing"),
    path("start_mailing/<int:pk>", start_mailing, name="start_mailing"),
    path("report/", ReportView.as_view(), name="report")
]
