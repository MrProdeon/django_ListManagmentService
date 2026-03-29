from django.contrib import admin
from django.urls import path
from mailing.views import MessageCreateView, MessageListView, MessageUpdateView, MessageDetailView, MessageDeleteView

app_name = "mailing"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", MessageListView.as_view(), name="list_message"),
    path("create_message/", MessageCreateView.as_view(), name="create_message"),
    path("update_message/<int:pk>", MessageUpdateView.as_view(), name="update_message"),
    path("detail_message/<int:pk>", MessageDetailView.as_view(), name="detail_message"),
    path("delete_message/<int:pk>", MessageDeleteView.as_view(), name="delete_message")
]
