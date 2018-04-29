from django.shortcuts import render
from django.http import HttpResponse
from .models import User


def index(request):
    all_users = User.objects.all()
    context = {'all_users': all_users}
    return render(request, 'social_network/index.html', context)


def detail(request, user_id):
    user = User.objects.filter(pk=user_id)[0]
    friends = user.friends.all()
    context = {'friends': friends}
    return render(request, 'social_network/friends.html', context)


def login(request):
    return render(request, 'social_network/home.html', {})


def home(request):
    return render(request, 'social_network/myhome.html', {})
