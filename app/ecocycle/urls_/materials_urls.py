from django.urls import path

from ..views import materials_views as views

app_name = "materials"
urlpatterns = [
    path("materials_new/", views.materials_new, name="materials_new"),
]