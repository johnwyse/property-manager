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

            return render(request, 'property/index.html', {
                "units": units,
            })
        else:
            try:
                my_unit = Unit.objects.get(tenant=request.user)
                empty_units = None
            except ObjectDoesNotExist: 
                my_unit = None
                empty_units = Unit.objects.filter(tenant=None)
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
        if 'image' in request.FILES:
            image = request.FILES["image"]
        else:
            image = None

        if 'lease' in request.FILES:
            lease = request.FILES["lease"]
        else:
            lease = None
        try:
            u = Unit(
                manager = User.objects.get(username=request.user),
                address = request.POST["address"],
                image = image,
                lease = lease
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
        if 'image' in request.FILES:
            image = request.FILES["image"]
        else:
            image = None
        try:
            i = Issue(
                unit_id = Unit.objects.get(tenant=reporter),
                title = request.POST["title"],
                image = image,
                description = request.POST["description"]
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
            if 'image' in request.FILES:
                image = request.FILES["image"]
            else:
                image = None
            try:
                m = Message(
                    image = image,
                    sender = User.objects.get(username=request.user),
                    recipient = User.objects.get(username=my_unit.manager),
                    text = request.POST["text"]
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
            if 'image' in request.FILES:
                image = request.FILES["image"]
            else:
                image = None
            try:
                m = Message(
                    sender = User.objects.get(username=request.user),
                    recipient = User.objects.get(username=User.objects.get(id=request.POST["tenant"])),
                    image = image,
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
def add_profile_picture(request):
    if request.method == "POST":
        if 'image' in request.FILES:
            profile_picture = request.FILES["image"]
        else:
            profile_picture = None
        user = User.objects.get(username=request.user)
        user.profile_picture = profile_picture
        user.save()
        return HttpResponseRedirect(reverse("profile"))
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
            
            # get number of unread messages to display
            unread_counts = []
            for unit in units:
                try:
                    unread_count = Message.objects.filter(read=False).filter(sender=unit.tenant).filter(recipient=request.user).count()
                except ObjectDoesNotExist:
                    unread_count = 0
                unread_counts.append(unread_count)
            
            zipped_messages_info = zip(unread_counts, units)
            
            return render(request, 'property/messages.html', {
                "messages_info": zipped_messages_info
            })
    else:
        return render(request, 'property/error.html')



@login_required
def unit_messages(request, unit_id):
    if request.method == "GET":
        try:
            unit = Unit.objects.get(id=unit_id)
        except ObjectDoesNotExist:
            return render(request, 'property/error.html')
        if request.user.manager:     
            messages = Message.objects.filter(sender=request.user).filter(recipient=unit.tenant) | Message.objects.filter(recipient=request.user).filter(sender=unit.tenant)
            ordered_messages = Message.objects.filter(id__in=messages).order_by('-timestamp')
            
            #Pagination
            paginator = Paginator(ordered_messages, 10) # Show 10 messages per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            # Render Unit Messages Page
            return render(request, 'property/unit_messages.html', {
                "messages": page_obj,
                "unit": unit,
                "data": unit_id
            })
        else:
            messages = Message.objects.filter(sender=request.user).values_list('id') | Message.objects.filter(recipient=request.user).values_list('id')
            ordered_messages = Message.objects.filter(id__in=messages).order_by('-timestamp')
            
            #Pagination
            paginator = Paginator(ordered_messages, 10) # Show 10 messages per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            # Render Unit Messages Page
            return render(request, 'property/unit_messages.html', {
                "messages": page_obj,
                "unit": unit,
                "data": unit_id
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
                unresolved_counts.append(unresolved_count)

            zipped_issues_info = zip(unresolved_counts, units)

            return render(request, 'property/issues.html', {
                "issues_info": zipped_issues_info
            })
    else:
        return render(request, 'property/error.html')


@login_required
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


@login_required
def profile(request):
    if request.method == "GET":
        user = User.objects.get(username=request.user)
        if user.tenant:
            try:
                units = Unit.objects.get(tenant=user)
            except ObjectDoesNotExist:
                units = None
        else:
            try:
                units = Unit.objects.filter(manager=user)
            except ObjectDoesNotExist:
                units = None
        return render(request, 'property/profile.html', {
            "user": user,
            "units": units
        })
    else:
        return render(request, 'property/error.html')



# API Route 
@csrf_exempt
@login_required
def edit_issue(request, issue_id):
    
    # Query for requested issue
    try:
        unit = Unit.objects.get(tenant=request.user)
        issue = Issue.objects.get(unit_id=unit.id, id=issue_id)
    except Issue.DoesNotExist:
        return JsonResponse({"error": "Issue not found."}, status=404)

    # Update issue description
    if request.method == "PUT":
        data = json.loads(request.body)
        issue.description = data["description"]
        issue.save()
        return HttpResponse(status=204)

    # Edit must be via PUT
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)



# API Route 
@csrf_exempt
@login_required
def delete_message(request, message_id):

    # Query for requested issue
    try:
        message = Message.objects.get(pk=message_id)
    except Issue.DoesNotExist:
        return JsonResponse({"error": "Message not found."}, status=404)

    # Delete message
    if request.method == "DELETE":
        message.delete()
        return HttpResponse(status=204)
    
    # Must be via DELETE
    else:
        return JsonResponse({"error": "DELETE request required."}, status=400)



# API Route 
@csrf_exempt
@login_required
def mark_as_read(request, unit_id):

    # Query for requested issue
    unit = Unit.objects.get(pk=unit_id)
    print(unit)
    try:
        messages = Message.objects.filter(recipient=request.user).filter(sender=unit.tenant).filter(read=False) | Message.objects.filter(recipient=request.user).filter(sender=unit.manager).filter(read=False)
        print(f"messages to be marked as read are {messages}")
    except Message.DoesNotExist:
        return JsonResponse({"error": "Messages not found."}, status=404)

    # Mark messages as read
    if request.method == "PUT":
        for message in messages:
            message.read = True
            message.save()
        return HttpResponse(status=204)
    
    # Must be via PUT
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)


# API Route 
@csrf_exempt
@login_required
def get_notifications(request):

    if request.method == "GET":
        if request.user.manager:
            # unread message count
            unread_messages_count = Message.objects.filter(recipient=request.user).filter(read=False).count()
            print(f"unread messages: {unread_messages_count}")
            
            # unresolved issues count
            try:
                units = Unit.objects.filter(manager=request.user)
            except ObjectDoesNotExist:
                units = None
            unresolved_issues_count = 0
            for unit in units:
                unit_unresolved_issues_count = Issue.objects.filter(unit_id=unit.id).filter(resolved=False).count()
                unresolved_issues_count += unit_unresolved_issues_count
            
            print(f"unresolved : {unresolved_issues_count}")
        
        else:
            unread_messages_count = Message.objects.filter(recipient=request.user).filter(read=False).count()
            unresolved_issues_count = 0
        
        data = {
            "unread": unread_messages_count,
            "unresolved": unresolved_issues_count
        }

        return JsonResponse(data, status=200)


    else: 
        return JsonResponse({"error": "GET request required."}, status=400)









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


