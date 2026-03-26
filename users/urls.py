from django.contrib import admin
from django.urls import path
from users.views import CreateUser, ListUser, DeleteUser

app_name = "users"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("create_user/", CreateUser.as_view(), name="create_user"),
    path("list_user/", ListUser.as_view(), name="list_user"),
    path("update_user/<int:pk>/", CreateUser.as_view(), name="update_user"),
    path("delete_user/<int:pk>/", DeleteUser.as_view(), name="delete_user")
]
