from django.urls import path
from ..views import api_views as views

app_name = "api"
urlpatterns = [
    path("", views.index, name="index"),
    path('procesos/', views.obtener_procesos, name='obtener_procesos'),
]