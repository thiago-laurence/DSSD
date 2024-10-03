from django.urls import path
from ..views import recolector_view as views

app_name = "recolector"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id_recolector>/recolecciones/", views.view_recolecciones, name="view_recolecciones"),
    path("recolecciones/<int:id_recoleccion>/close/", views.close_recoleccion, name="close_recoleccion"),
    path("recolecciones/add/", views.add_recoleccion, name="add_recoleccion"),
]