from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("coach_dashboard/", include("coach_dashboard.urls")),
    path("athlete_dashboard/", include("athlete_dashboard.urls")),
]