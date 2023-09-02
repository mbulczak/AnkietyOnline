from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("user-login/", views.user_login, name="user_login"),
    path("user-logout/", views.user_logout, name="user_logout"),
    path("user-register/", views.user_register, name="user_register"),
    path("edit-user/", views.edit_user, name="edit_user"),
    path("change-password/", views.change_password, name="change_password"),
]
