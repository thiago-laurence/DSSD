from django.urls import path
from ..views import recoleccion_views as views

app_name = "recoleccion"
urlpatterns = [
    path("<int:id_recoleccion>/", views.view_recoleccion, name="view"),
    path("update/", views.update_recoleccion, name="update"),
]