from django.urls import path
from ..views import recolector_view as views

app_name = "recolector"
urlpatterns = [
    path("", views.index, name="index"),
]