from django.urls import path

from . import views

app_name = "home"
urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login", views.login_view, name="login"),
    path("accounts/logout", views.logout_view, name="logout"),
    path("coach_dashboard/<int:athlete_pk>/new", views.create_training_plan, name="create_training_plan"),
    path("coach_dashboard/<int:athlete_pk>", views.training_plans_list, name="training_plans_list"),
    path("coach_dashboard", views.coach_dashboard, name="coach_dashboard"),
    path("athlete_dashboard", views.athlete_dashboard, name="athlete_dashboard"),
]