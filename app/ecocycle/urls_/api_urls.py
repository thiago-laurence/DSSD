from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from ..views import api_views as views

app_name = "api"
urlpatterns = [
    path("login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("pedidos", views.get_pedidos, name="get_pedidos"),
    path('pedidos/add', views.add_pedido, name='add_pedido'),
    path('centros', views.get_centros, name='get_centros'),
    path('depositos/add', views.add_deposito, name='add_deposito')
]