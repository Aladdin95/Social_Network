from django.shortcuts import render
from django.http import HttpResponse
from .models import User


def index(request):
    all_users = User.objects.all()
    context = {'all_users': all_users}
    return render(request, 'social_network/home.html', context)


def detail(request, user_id):
    user = User.objects.filter(pk=user_id)[0]
    friends = user.friends.all()
    context = {'friends': friends}
    return render(request, 'social_network/friends.html', context)

    #for friend in friends:
    #    html += " " + friend + " "
    #return HttpResponse(html)
    #return HttpResponse("<h2>"+user_id+"</h2>")
    #+'<br /'+'</p>'