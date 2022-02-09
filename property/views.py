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
    if request.user.is_authenticated:
        if request.user.manager:
            try:
                units = Unit.objects.filter(manager=request.user).order_by('address').order_by('-tenant')
            except ObjectDoesNotExist:
                units = None
            print(units)
            return render(request, 'property/index.html', {
                "units": units
            })
        else:
            try:
                my_unit = Unit.objects.get(tenant=request.user)
                empty_units = None
            except ObjectDoesNotExist: 
                my_unit = None
                empty_units = Unit.objects.filter(tenant=None)
            print(my_unit)
            return render(request, 'property/index.html', {
                "my_unit": my_unit,
                "empty_units": empty_units
            })
    else:
        return render(request, 'property/login.html')


@login_required
def add_tenant(request):
    if request.method == "POST":
        if request.user.tenant:
            try:
                unit = Unit.objects.get(id=request.POST["chosen_unit"])
                unit.tenant = request.user
                unit.save()
            except ValueError:
                return render(request, "property/error.html")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'property/error.html')


@login_required
def change_resolved(request, issue_id):
    if request.method == "POST":
        if request.user.tenant:
            try:
                issue = Issue.objects.get(id=issue_id)
                if issue.resolved == True:
                    issue.resolved = False
                else:
                    issue.resolved = True
                issue.save()
            except ValueError:
                return render(request, "property/error.html")
        return HttpResponseRedirect(reverse("issues"))
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
            return render(request, "property/add_property.html", {
                "add_message": "Must provide an address"
            })

        u.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "property/add_property.html")


@login_required
def report_issue(request):
    if request.method =="POST":
        reporter = User.objects.get(username=request.user)
        try:
            i = Issue(
                unit_id = Unit.objects.get(tenant=reporter),
                title = request.POST["title"],
                image = request.POST["image"],
                description = request.POST["description"],
            )
        except ValueError:
            return render(request, "property/error.html", {
                "message": "Invalid Issue. Try again."
            })
        i.save()
        return HttpResponseRedirect(reverse("issues"))
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
def send_message(request):
    if request.method =="POST":
        if request.user.tenant == True:
            my_unit = Unit.objects.get(tenant=request.user)
            try:
                m = Message(
                    sender = User.objects.get(username=request.user),
                    recipient = User.objects.get(username=my_unit.manager),
                    image = request.POST["image"],
                    text = request.POST["text"],
                )
            except ValueError:
                return render(request, "property/error.html", {
                    "message": "Invalid message. Try again."
                })
            m.save()
            return HttpResponseRedirect(reverse("messages"))
        else:
            # if manager is sending to tenant
            unit = Unit.objects.get(tenant=request.POST["tenant"])
            try:
                m = Message(
                    sender = User.objects.get(username=request.user),
                    recipient = User.objects.get(username=User.objects.get(id=request.POST["tenant"])),
                    image = request.POST["image"],
                    text = request.POST["text"],
                )
            except ValueError:
                return render(request, "property/error.html", {
                    "message": "Invalid message. Try again."
                })
            m.save()
            return HttpResponseRedirect(reverse("unit_messages", kwargs={'unit_id': unit.id}))
    else:
        return HttpResponseRedirect(reverse("index"))



@login_required
def unit(request, unit_id):
    if request.method == "GET":
        unit = Unit.objects.get(id=unit_id)
        return render(request, 'property/unit.html', {
            "unit": unit
        })

@login_required
def messages(request):
    if request.method == "GET":
        if request.user.tenant == True:
            try:
                unit_count = Unit.objects.filter(tenant=request.user).count()
            except ObjectDoesNotExist:
                unit_count = 0
            print(unit_count)
            if unit_count != 1:
                return render(request, 'property/messages.html')
            else:
                unit = Unit.objects.get(tenant=request.user)
                return HttpResponseRedirect(reverse("unit_messages", kwargs={'unit_id': unit.id}))
        else:
            # manager loads links to messages with each tenant/unit
            try:
                units = Unit.objects.filter(manager=request.user).exclude(tenant=None).order_by('-tenant')
            except ObjectDoesNotExist:
                units = None
            return render(request, 'property/messages.html', {
                "units": units
            })
    else:
        return render(request, 'property/error.html')

@login_required
def unit_messages(request, unit_id):
    if request.method == "GET":
        unit = Unit.objects.get(id=unit_id)
        if request.user.manager:     
            messages = Message.objects.filter(sender=request.user).filter(recipient=unit.tenant) | Message.objects.filter(recipient=request.user).filter(sender=unit.tenant)
            ordered_messages = Message.objects.filter(id__in=messages).order_by('-timestamp')
            return render(request, 'property/unit_messages.html', {
                "messages": ordered_messages,
                "unit": unit
            })
        else:
            messages = Message.objects.filter(sender=request.user).values_list('id') | Message.objects.filter(recipient=request.user).values_list('id')
            ordered_messages = Message.objects.filter(id__in=messages).order_by('-timestamp')
            return render(request, 'property/unit_messages.html', {
                "messages": ordered_messages,
                "unit": unit
            })


    else:
        return render(request, 'property/error.html')

@login_required
def issues(request):
    if request.method == "GET":
        if request.user.tenant:
            try:
                unit_count = Unit.objects.filter(tenant=request.user).count()
            except ObjectDoesNotExist:
                unit_count = 0
            print(unit_count)
            if unit_count != 1:
                return render(request, 'property/issues.html')
            else:
                unit = Unit.objects.get(tenant=request.user)
                return HttpResponseRedirect(reverse("unit_issues", kwargs={'unit_id': unit.id}))
        else:
            try:
                units = Unit.objects.filter(manager=request.user).exclude(tenant=None).order_by('address')
            except ObjectDoesNotExist:
                units = None
            
            unresolved_counts = []
            for unit in units:
                try:
                    unresolved_count = Issue.objects.filter(unit_id=unit.id).filter(resolved=False).count()
                except ObjectDoesNotExist:
                    unresolved_count = None
                print(unresolved_count)
                unresolved_counts.append(unresolved_count)
            
            print(unresolved_counts)
            print(units)

            zipped_issues_info = zip(unresolved_counts, units)

            return render(request, 'property/issues.html', {
                "issues_info": zipped_issues_info
            })

    else:
        return render(request, 'property/error.html')


def unit_issues(request, unit_id):
    if request.method == "GET":
        unit = Unit.objects.get(id=unit_id)
        resolved_issues = Issue.objects.filter(unit_id=unit.id).filter(resolved=True).order_by('-time_created') 
        unresolved_issues = Issue.objects.filter(unit_id=unit.id).filter(resolved=False).order_by('-time_created') 
        return render(request, 'property/unit_issues.html', {
            "resolved_issues": resolved_issues,
            "unresolved_issues": unresolved_issues,
            "unit": unit
        })
    else:
        return render(request, 'property/error.html')



def profile(request):
    if request.method == "GET":
        user = User.objects.get(username=request.user)
        return render(request, 'property/profile.html', {
            "user": user
        })
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
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
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
        
        if username == "" or first_name == "" or last_name == "" or email == "" or password == "":
            return render(request, "property/register.html", {
                "message": "Must enter username, email, full name, and password."
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
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            return render(request, "property/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "property/register.html")


