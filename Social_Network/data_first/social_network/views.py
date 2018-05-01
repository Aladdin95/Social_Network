from django.shortcuts import render,redirect
from django.contrib.auth import  authenticate, login
from django.views import generic
from django.views.generic import View
from django.http import HttpResponse
from social_network.models import User
from .forms import UserForm




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


class UserFormView(View):
    form_class= UserForm
    template_name='social_network/register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #user.set_password(password)
            user.save()
            #user=authenticate(username=username,password=password)
            if user is not None:
               # if user.active:
                #login(request,user)
                return redirect('home')

        return render(request,self.template_name,{'form':form})
