from django.shortcuts import render
from django.http import HttpResponse
from .models import User


def index(request):
    all_users = User.objects.all()
    html = ''
    for user in all_users:
        url = '/home/'+str(user.pk)+'/'
        html += '<a href="' + url + '">' + user.First_name+" " + user.Last_name + '</a><br>'
    return HttpResponse(html)


def detail(request, user_id):
    user = User.objects.filter(pk=user_id)[0]
    friends = user.friends.all()
    return HttpResponse(friends)

    #for friend in friends:
    #    html += " " + friend + " "
    #return HttpResponse(html)
    #return HttpResponse("<h2>"+user_id+"</h2>")
    #+'<br /'+'</p>'