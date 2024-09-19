from django.urls import path, include

urlpatterns = [
    # Index page for the app
    path("", include("ecocycle.urls_.home_urls")),

    # Login urls
    path("login/", include("ecocycle.urls_.login_urls")),

    # Recolector urls
    path("recolector/", include("ecocycle.urls_.recolector_urls")),
]