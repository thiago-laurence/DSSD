from django.urls import path
from ..views import centro_views as views

app_name = "centro"
urlpatterns = [
    path("", views.index, name="index"),
    path("perfil", views.view_perfil, name="view_perfil"),
    path("pedidos", views.list_pedidos, name="list_pedidos"),
    path('pedidos/assign', views.asignar_pedido, name='assign_pedido')
]