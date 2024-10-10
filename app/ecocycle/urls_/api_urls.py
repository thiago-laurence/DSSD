from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from ..views import api_views as views

app_name = "api"
urlpatterns = [
    path("hello/", views.hello, name="hello"),
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("pedidos/", views.get_pedidos, name="get_pedidos"),
]