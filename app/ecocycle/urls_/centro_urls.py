from django.urls import path
from ..views import centro_views as views

app_name = "centro"
urlpatterns = [
    path("", views.index, name="index"),
]