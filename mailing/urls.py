from django.contrib import admin
from django.urls import path
from mailing.views import MessageCreateView, MessageListView, MessageUpdateView

app_name = "mailing"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", MessageListView.as_view(), name="list_message"),
    path("create/", MessageCreateView.as_view(), name="create_message"),
    path("update/<int:pk>", MessageUpdateView.as_view(), name="update_message")
]
