from django.urls import path

from . import views

app_name = "home"
urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login", views.login_view, name="login"),
    path("accounts/logout", views.logout_view, name="logout"),
    path("coach_dashboard", views.coach_dashboard, name="coach_dashboard"),
    path("athlete_dashboard", views.athlete_dashboard, name="athlete_dashboard"),
]