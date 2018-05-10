from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views import generic
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from .models import CustomUser, Mypost
from .forms import CustomUserCreationForm
from itertools import chain


def index(request):
    all_users = CustomUser.objects.all()
    context = {'all_users': all_users}
    return render(request, 'social_network/index.html', context)


def detail(request, username):
    user = CustomUser.objects.get(username=username)
    friends = user.friends.all()
    return render(request, 'social_network/friends.html', {'friends': friends})


def add_friend(request, username):
    user = CustomUser.objects.get(username=username)
    new_friend = CustomUser.objects.get(username=request.POST['Friend'])
    user.friends.add(new_friend)
    user.save()
    return render(request, 'social_network/friends.html', {'friends': user.friends.all()})


def profile(request, username):
    user = CustomUser.objects.get(username=username)
    return render(request, 'social_network/profile.html', {'user': user})


class Home(View):
    template = 'social_network/myhome.html'

    def get(self, request):
        if request.user.is_authenticated:
            posts = request.user.mypost_set.all()
            posts_list = list(chain(posts))
            for user in request.user.friends.all():
                posts_list += list(chain(user.mypost_set.all()))
            posts_list = sorted(posts_list, key=lambda instance: instance.updated, reverse=True)
            return render(request, self.template, {'posts': posts_list})
        return render(request, self.template, {})

    def post(self, request):
        if 'postbody' in request.POST:
            new_post = Mypost()
            new_post.postbody = request.POST['postbody']
            new_post.user = request.user
            new_post.save()
            return redirect(request.path_info)

        elif 'like' in request.POST:
            post = Mypost.objects.get(pk=request.POST['post_id'])
            post.likes.add(request.user)
            post.save()
            return redirect('/')


class UserFormView(View):
    form_class = CustomUserCreationForm
    template_name = 'social_network/Registration.html'
    error = 'social_network/error.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            new_user = authenticate(username=username, password=password)
            if new_user is not None:
                if new_user.is_active:
                    auth_login(request, new_user)
            return redirect('home')
        return render(request, self.error, {'form': form})
