from datetime import datetime

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404

from .forms import TrainingPlanForm

from .models import Athlete, Coach, TrainingPlan, TrainingDay

def index(request):
    return render(request, "home/index.html", {
        "is_athlete": Athlete.objects.filter(user__username=request.user).exists(),
        "is_coach": Coach.objects.filter(user__username=request.user).exists(),
    })

def coach_dashboard(request):
    return render(request, "home/coach_dashboard.html", {"coached_athletes": Athlete.objects.filter(coach__user__pk=request.user.pk)})

def training_plans_list(request, athlete_pk):
    athlete = get_object_or_404(Athlete, pk=athlete_pk)
    coach = get_object_or_404(Coach, user__pk=request.user.pk)
    training_plans = TrainingPlan.objects.filter(athlete__pk=athlete.pk, coach__pk=coach.pk)
    return render(request, "home/training_plans_list.html", {"athlete": athlete, "training_plans": training_plans})

def create_training_plan(request, athlete_pk):
    if request.method == "POST":
        new_plan_form = TrainingPlanForm(request.POST)
        if new_plan_form.is_valid():
            new_plan = TrainingPlan(
                athlete=get_object_or_404(Athlete, pk=athlete_pk), 
                coach=get_object_or_404(Coach, user__pk=request.user.pk),
                start_date=new_plan_form.cleaned_data['start_date'],
                end_date=new_plan_form.cleaned_data['end_date']
            )
            new_plan.save()
            return HttpResponseRedirect(reverse("home:training_plans_list", args=(athlete_pk,)))
    else:
        new_plan_form = TrainingPlanForm()
    return render(request, "home/create_training_plan.html", {"athlete": get_object_or_404(Athlete, pk=athlete_pk), "new_plan_form": new_plan_form})


def athlete_dashboard(request):
    return render(request, "home/athlete_dashboard.html", {})

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("home:index"))
    else:
        return HttpResponseRedirect(reverse("home:index"))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home:index"))