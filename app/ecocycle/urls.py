from django.urls import path, include

urlpatterns = [
    # Index page for the app
    path("", include("ecocycle.urls_.home_urls")),

    # Auth urls
    path("login/", include("ecocycle.urls_.login_urls")),
]