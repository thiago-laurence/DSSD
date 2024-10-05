from django.urls import path
from ..views import centro_views as views

app_name = "centro"
urlpatterns = [
    path("", views.index, name="index"),
    path("perfil/<int:id_centro>", views.view_perfil, name="view_perfil"),
]