from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

def index(request):
    template = loader.get_template("home/index.html")
    return HttpResponse(template.render({}, request))

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