import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Issue, Message, Unit


def index(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            if request.user.manager:
                try:
                    units = Unit.objects.filter(manager=request.user)
                except ObjectDoesNotExist:
                    units = None
                print(units)
                return render(request, 'property/index.html', {
                    "units": units
                })
            else:
                try:
                    my_unit = Unit.objects.get(tenant=request.user)
                except ObjectDoesNotExist: 
                    my_unit = None
                print(my_unit)
                return render(request, 'property/index.html', {
                    "my_unit": my_unit
                })
        else:
            return render(request, 'property/login.html')
    else:
        return render(request, 'property/error.html')

@login_required
def add_property(request):
    if request.method =="POST":
        try:
            u = Unit(
                manager = User.objects.get(username=request.user),
                address = request.POST["address"],
                image = request.POST["image"]
            )
        except ValueError:
            return render(request, "property/error.html", {
                "message": "Invalid Property"
            })
        if u.address == "":
            return render(request, "property/index.html", {
                "add_message": "Must provide an address"
            })

        u.save()
        return HttpResponseRedirect(reverse("index"))

def messages(request):
    if request.method == "GET":
        return render(request, 'property/messages.html')
    else:
        return render(request, 'property/error.html')


def issues(request):
    if request.method == "GET":
        return render(request, 'property/issues.html')
    else:
        return render(request, 'property/error.html')


def profile(request):
    if request.method == "GET":
        return render(request, 'property/profile.html')
    else:
        return render(request, 'property/error.html')




# Login, Logout, Register views edited from CS50W Project4 distribution code

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "property/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "property/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        user_type = request.POST["user_type"]
        print(user_type)
        if user_type == "tenant":
            tenant = True
            manager = False
        else:
            tenant = False
            manager = True
        
        if username == "" or email == "" or password == "":
            return render(request, "property/register.html", {
                "message": "Must enter username, email, and password."
            })    

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "property/register.html", {
                "message": "Passwords must match."
            }) 

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.tenant = tenant
            user.manager = manager
            user.save()
        except IntegrityError:
            return render(request, "property/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "property/register.html")


