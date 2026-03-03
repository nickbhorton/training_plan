from django.urls import path

from . import views

app_name = "home"
urlpatterns = [
    path("", views.index, name="index"),
    path("plan/add", views.add_plan, name="add_plan"),
    path("plan/<int:pk>/change", views.change_plan, name="change_plan"),
    path("plan/<int:pk>/delete", views.delete_plan, name="delete_plan"),
    path("plan/<int:pk>/detail", views.plan_detail, name="plan_detail"),
    path("plan/<int:plan_pk>/day/<int:day_count>/add" , views.add_day, name="add_day"),
    path("accounts/login", views.login_view, name="login"),
    path("accounts/logout", views.logout_view, name="logout"),
]