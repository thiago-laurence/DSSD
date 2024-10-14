from django.urls import path
from ..views import administrador_views as views

app_name = "administrador"
urlpatterns = [
    path("", views.index, name="index"),
    path("materiales", views.view_materiales, name="materiales"),
    path("materiales/add", views.add_material, name="add_material"),
    path("puntos", views.view_puntos, name="puntos"),
    path("puntos/add", views.add_punto, name="add_punto"),
    path("centros", views.view_centros, name="centros"),
    path("centros/add", views.add_centro, name="add_centro"),
]