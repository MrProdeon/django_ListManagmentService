from django.contrib import admin
from django.urls import path
from users.views import CreateUser

app_name = "users"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("create_user", CreateUser.as_view(), name="create_user")
]
