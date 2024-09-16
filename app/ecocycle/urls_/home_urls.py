from django.urls import path

from ..views import home_views as views

app_name = "home"
urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
]