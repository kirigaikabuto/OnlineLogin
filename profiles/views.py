from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import ProfileCreationForm
from .models import *
from django.contrib.auth import authenticate, login, logout


def register_page(request):
    user_form = None
    profile_form = None
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileCreationForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            my_user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = my_user
            profile.save()
            return HttpResponse('ok post accepted')

    user_form = UserCreationForm()
    profile_form = ProfileCreationForm()
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "profiles/register.html", context)


def login_page(request):
    error = ""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            error = "нет такого пользователя"
        else:
            login(request, user)
            return redirect("profile_page")
    context = {
        "error": error
    }
    return render(request, "profiles/login.html", context=context)


def profile_page(request):
    userObject = request.user
    profile = Profile.objects.get(user=userObject)
    profiles = Profile.objects.all().exclude(user=profile.user)
    orderToFriend = OrderToFriend.objects.all().filter(from_profile=profile)
    free_profiles = []

    for i in profiles:
        DoesntExist = True
        for j in orderToFriend:
            if i == j.to_profile:
                DoesntExist = False
        if DoesntExist:
            free_profiles.append(i)

    orderToMe = OrderToFriend.objects.all().filter(to_profile=profile, accept=False)
    n = len(orderToMe)
    friends = OrderToFriend.objects.all().filter(to_profile=profile, accept=True)
    n_friends = len(friends)
    context = {
        "profile": profile,
        "all_profiles": free_profiles,
        "count_orders": n,
        "count_friends": n_friends,
    }

    return render(request, "profiles/profile.html", context=context)


def order_friend_action(request, profile_pk):
    from_user = request.user
    from_profile = Profile.objects.get(user=from_user)
    to_profile = Profile.objects.get(pk=profile_pk)
    order_friend = OrderToFriend(from_profile=from_profile, to_profile=to_profile)
    order_friend.save()
    return redirect("profile_page")


def log_out(request):
    logout(request)
    return redirect("login_page")


def list_incoming_requests(request):
    userObject = request.user
    profile = Profile.objects.get(user=userObject)
    incomingRequests = OrderToFriend.objects.all().filter(to_profile=profile, accept=False)
    context = {
        "orders": incomingRequests,
    }
    return render(request, "profiles/list_incoming_requests.html", context=context)


def incoming_request_accept(request, id):
    order = OrderToFriend.objects.get(pk=id)
    order.accept = True
    order.save()
    return redirect("list_incoming_requests")

def list_friends(request):
    userObject = request.user
    profile = Profile.objects.get(user=userObject)
    friends = OrderToFriend.objects.all().filter(to_profile=profile, accept=True)
    context = {
        "friends": friends,
    }
    return render(request,"profiles/list_friends.html", context = context)

def incoming_request_cancel(request, id):
    order = OrderToFriend.objects.get(pk=id)
    order.delete()
    return redirect("list_incoming_requests")

def private_room(request):
    userObject = request.user
    profile = Profile.objects.get(user=userObject)
    context = {
        "profile": profile,
    }
    return render(request,"profiles/private_room.html", context = context)