from django.urls import path, include

urlpatterns = [
    # Index page for the app
    path("", include("ecocycle.urls_.home_urls")),

    # Login urls
    path("login/", include("ecocycle.urls_.login_urls")),
    
    # Material urls
    path("materials/", include("ecocycle.urls_.materials_urls")),

    # Recolector urls
    path("recolector/", include("ecocycle.urls_.recolector_urls")),
    
    # Centros urls
    path("centro/", include("ecocycle.urls_.centro_urls")),

    # Recoleccion urls
    path("recoleccion/", include("ecocycle.urls_.recoleccion_urls")),

    # Administrador urls
    path("administrador/", include("ecocycle.urls_.administrador_urls")),

    # Bonita urls
    path("bonita/", include("ecocycle.urls_.bonita_urls")),

    # API urls
    path("api/", include("ecocycle.urls_.api_urls")),
]

handler404 = 'views.error_views.error_404'