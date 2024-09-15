from django.urls import path

from ..views import login_views as views

app_name = "login"
urlpatterns = [
    path("", views.login, name="index"),
    path("auth/", views.auth, name="auth"),
]