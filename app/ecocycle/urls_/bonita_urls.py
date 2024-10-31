from django.urls import path
from ..views import bonita_views as views

app_name = "bonita"
urlpatterns = [
    path("", views.index, name="index"),
    path('procesos/', views.carga_material_recolectado, name='cargo_material_recolectado'),
]