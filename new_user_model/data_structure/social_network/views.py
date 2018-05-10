from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views import generic
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from .models import CustomUser, Mypost
from .forms import CustomUserCreationForm
from itertools import chain
from django.db.models import CharField
from django.db.models import  Q


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
            for user in request.user.friends.all():
                posts |= user.mypost_set.all()
            posts = sorted(posts, key=lambda instance: instance.created, reverse=True)
            return render(request, self.template, {'posts': posts})
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
            return redirect('/#'+str(post.pk))

        elif 'search' in request.POST:
            word = request.POST['search']
            search_list = CustomUser.objects.filter(first_name__icontains=word)
            search_list |= CustomUser.objects.filter(last_name__icontains=word)
            search_list |= CustomUser.objects.filter(username__icontains=word)
            search_list |= CustomUser.objects.filter(email=word)
            search_list |= CustomUser.objects.filter(mobile_number=word)
            # search_list = list(chain(search_list))
            return render(request, 'social_network/test.html', {'search_list': search_list})


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
