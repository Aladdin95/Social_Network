from . import views
from django.urls import path
from django.conf.urls import include, url


urlpatterns = [
    #/users/
    # url(r'(?P<username>[\w.@+-]+)/add_post/$', views.add_post, name='add_post'),
    url(r'graph/$', views.graph, name='graph'),
    url(r'reg/$', views.UserFormView.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
    url(r'^(?P<username>[\w.@+-]+)/friends/$', views.detail, name='detail'),
    url(r'(?P<username>[\w.@+-]+)/friends/add_friend/$', views.add_friend, name='add_friend'),
    url(r'^users', views.index, name='index'),
    # url(r'^login', views.login, name='index'),
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^(?P<username>[\w.@+-]+)/$', views.Profile.as_view(), name='profile'),
]
