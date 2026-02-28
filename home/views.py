from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .models import Athlete, Coach

import json

def index(request):
    template = loader.get_template("home/index.html")
    return HttpResponse(template.render({
        "is_athlete": Athlete.objects.filter(user__username=request.user).exists(),
        "is_coach": Coach.objects.filter(user__username=request.user).exists(),
    },request))

def coach_dashboard(request):
    coached_athletes = Athlete.objects.filter(coach__user__username=request.user.username)
    template = loader.get_template("home/coach_dashboard.html")
    return HttpResponse(template.render({"coached_athletes": coached_athletes},request))

def athlete_dashboard(request):
    template = loader.get_template("home/athlete_dashboard.html")
    return HttpResponse(template.render({},request))

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