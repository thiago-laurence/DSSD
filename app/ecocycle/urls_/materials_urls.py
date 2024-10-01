from django.urls import path
from ..views import materials_views as views

app_name = "materials"
urlpatterns = [
    path("", views.index, name="index"),
    path("send/", views.send, name="send"),
]