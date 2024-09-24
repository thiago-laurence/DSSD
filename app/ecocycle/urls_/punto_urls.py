from django.urls import path
from ..views import punto_views as views

app_name = "punto"
urlpatterns = [
    path("", views.index, name="index"),
]