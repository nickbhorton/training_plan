from datetime import timedelta, date, datetime

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404

from .forms import TrainingPlanForm, TrainingDayForm

from .models import Athlete, Coach, TrainingPlan, TrainingDay

def index(request):
    if not request.user.is_anonymous:
        is_athlete = Athlete.objects.filter(user=request.user).exists()
        is_coach = Coach.objects.filter(user=request.user).exists()
        coach_plans = TrainingPlan.objects.filter(coach__user=request.user)
        return render(request, "home/index.html", {
            "is_athlete": is_athlete,
            "is_coach": is_coach,
            "coach_plans": coach_plans 
        })
    return render(request, "home/index.html", {
        "is_athlete": False,
        "is_coach": False,
        "coach_plans": [] 
    })

def add_day(request, plan_pk, day_count):
    plan = get_object_or_404(TrainingPlan, pk=plan_pk)
    if request.method == "POST":
        form = TrainingDayForm(request.POST)
        if form.is_valid():
            day = form.save(commit = False)
            day.plan = plan
            day.date = plan.start_date + timedelta(days=day_count) 
            day.save()
            return HttpResponseRedirect(reverse("home:plan_detail", args=(plan_pk,)))
    else:
        form = TrainingDayForm()
    return render(request, "home/add_day.html", {"form": form, "plan_pk": plan_pk, "day_count": day_count})


def plan_detail(request, pk):
    plan = get_object_or_404(TrainingPlan, pk=pk)
    # create all days
    days: list[dict] = []
    for i in range((plan.end_date - plan.start_date).days + 1):
        date_delta = plan.start_date + timedelta(days=i)
        days.append({"date": date_delta, "count": i, "training_day": None})

    # get TrainingDay objects
    training_days = TrainingDay.objects.filter(plan__pk=pk)
    day_count_training_day_tuples = []
    for day in training_days:
        day_count_training_day_tuples.append(((day.date - plan.start_date).days, day))

    # put TrainingDay objects into days
    for i, training_day in day_count_training_day_tuples:
        days[i]["training_day"] = training_day

    weeks: list[list[dict]] = []
    week: list[dict] = []
    for i, day in enumerate(days):
        week.append(day)
        if day["date"].weekday() == 6:
            weeks.append(week)
            week = []
    if len(week) > 0:
        weeks.append(week)
    return render(request, "home/plan_detail.html", {"plan": plan, "weeks": weeks})

def add_plan(request):
    if request.method == "POST":
        form = TrainingPlanForm(request.POST, user=request.user)
        if form.is_valid():
            plan = form.save(commit = False)
            plan.coach = get_object_or_404(Coach, user=request.user)
            plan.save()
            return HttpResponseRedirect(reverse("home:index"))
    else:
        form = TrainingPlanForm(user=request.user)
    return render(request, "home/add_plan.html", {"form": form})

def change_plan(request, pk):
    plan = get_object_or_404(TrainingPlan, pk=pk, coach__user=request.user)
    if request.method == "POST":
        form = TrainingPlanForm(request.POST, user=request.user, instance=plan)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("home:index"))
    else:
        form = TrainingPlanForm(user=request.user, instance=plan)
    return render(request, "home/change_plan.html", {"form": form, "pk": pk})

def delete_plan(request, pk):
    plan = get_object_or_404(TrainingPlan, pk=pk, coach__user=request.user)
    if request.method == "POST":
        plan.delete()
        return HttpResponseRedirect(reverse("home:index"))
    return render(request, "home/delete_plan.html", {"plan": plan, "pk": pk})

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