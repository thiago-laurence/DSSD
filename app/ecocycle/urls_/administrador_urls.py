from django.urls import path
from ..views import administrador_views as views

app_name = "administrador"
urlpatterns = [
    path("", views.index, name="index"),
    path("administrador/materiales", views.view_materiales, name="materiales"),
    path("administrador/materiales/add", views.add_material, name="add_material"),
    path("administrador/puntos", views.view_puntos, name="puntos"),
    path("administrador/puntos/add", views.add_punto, name="add_punto"),
    path("administrador/centros", views.view_centros, name="centros"),
    path("administrador/centros/add", views.add_centro, name="add_centro"),
]