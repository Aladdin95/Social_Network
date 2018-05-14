from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views import generic
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from .models import CustomUser, Mypost
from .forms import CustomUserCreationForm
from itertools import chain
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
#import common_neighbors



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


def graph(request):
    G = nx.DiGraph()

    for user in CustomUser.objects.all():
        G.add_node(user.username)
    for user in CustomUser.objects.all():
        for friend in user.friends.all():
            G.add_edge(user.username, friend.username)
    # nx.draw(G, with_labels=True)


    nx.draw_shell(G, with_labels=True, node_color='#80bfff', arrows=False, font_size=12,
                  node_size=500, edge_color='black')

    # nx.draw_networkx_labels(G, pos)
    # nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
    # nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)
    # plt.scatter(10, 10, alpha=10)
    plt.draw()
    # plt.scatter(0.01,0.01)
    plt.show()
    return redirect('home')

def shortestpath(request):
    G = nx.Graph()
    #all_simple_paths(G, source, target, cutoff=3):

    for user in CustomUser.objects.all():
        G.add_node(user.username)
    for user in CustomUser.objects.all():
        for friend in user.friends.all():
            G.add_edge(user.username, friend.username, color='black')

    paths_colors=['blue','violet','pink','purple']
    paths = nx.all_shortest_paths(G, request.POST['msgfrom'], request.POST['msgto'])

    loop_count = 0
    for path in paths:
        indx = loop_count % len(paths_colors)
        loop_count += 1
        for x in range(0, len(list(path))-1):
            G.edges[path[x], path[x+1]]['color'] = paths_colors[indx]

    edges = G.edges()
    colors = [G[u][v]['color'] for u, v in edges]

    nx.draw_shell(G, with_labels=True, node_color='#80bfff', arrows=False, font_size=12,
                     node_size=500, edge_color=colors)
    # temp = list(nx.common_neighbors(G, 'samy', 'abbas'))
    #nx.draw_networkx_labels(G, pos)
    #nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
    #nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)
    #plt.scatter(10, 10, alpha=10)
    plt.draw()
    #plt.scatter(0.01,0.01)
    plt.show()
    return redirect('home')
    # return render(request, 'social_network/graph.html', {'paths': len(temp)})






class Profile(View):
    profile = 'social_network/profile.html'
    myprofile = 'social_network/myprofile.html'










    def get(self, request, username):

        G = nx.Graph()

        for user in CustomUser.objects.all():
            G.add_node(user.username)
        for user in CustomUser.objects.all():
            for friend in user.friends.all():
                G.add_edge(user.username, friend.username)

        myuser = request.user
        touser = user


        user = CustomUser.objects.get(username=username)

        temp = list(nx.common_neighbors(G,user.username, request.user.username))
        if request.user == user:
            return render(request, self.myprofile, {'user': user})
        return render(request, self.profile, {'user': user, 'count': len(temp), 'paths': temp})

    def post(self, request, username):
        user = CustomUser.objects.get(username=username)
        if 'addfriend' in request.POST:
            user.friends.add(request.user)

        elif 'unfriend' in request.POST:
            user.friends.remove(request.user)

        user.save()
        return redirect(request.path_info)


class Home(View):
    template = 'social_network/myhome.html'
    signin_template='social_network/Registration.html'
    search_template = 'social_network/test.html'


    def get(self, request):
        search = request.GET.get('search')
        if search:
            search_list = CustomUser.objects.none()

            for word in search.split():
                search_list |= CustomUser.objects.filter(
                    Q(first_name__icontains=word) |
                    Q(last_name__icontains=word) |
                    Q(username__icontains=word) |
                    Q(email=word) |
                    Q(mobile_number=word)
                )


            return render(request, self.search_template, {'search_list': search_list })

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

        if 'like' in request.POST:
            post = Mypost.objects.get(pk=request.POST['post_id'])
            post.likes.add(request.user)
            post.save()
            return redirect('/#'+str(post.pk))

        if 'unlike' in request.POST:
            post = Mypost.objects.get(pk=request.POST['post_id'])
            post.likes.remove(request.user)
            post.save()
            return redirect('/#' + str(post.pk))

        if 'LikesCount' in request.POST:
            post = Mypost.objects.get(pk=request.POST['post_id'])
            users = post.likes.all()
            return render(request, 'social_network/likes_list.html', {'users': users})


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
